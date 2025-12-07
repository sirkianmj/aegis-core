import struct
import logging
from enum import Enum
from typing import List, Optional, Deque
from collections import deque
from pydantic import BaseModel

# Configure structured logging
logger = logging.getLogger("HATL")

class Architecture(Enum):
    INTEL_X64 = "INTEL_PT"
    ARM_V8 = "CORESIGHT_ETM"

class PacketType(Enum):
    BRANCH_DECISION = "TNT"   # Taken / Not Taken
    TARGET_IP = "TIP"         # Target Instruction Pointer
    CONTEXT_ID = "CID"        # Process ID (OS Context)
    OVERFLOW = "OVF"          # Data loss marker

class TracePacket(BaseModel):
    """
    Normalized Data Structure.
    The rest of AEGIS uses this, regardless of CPU type.
    """
    type: PacketType
    taken: Optional[bool] = None
    address: Optional[int] = None
    timestamp: float = 0.0

class RingBuffer:
    """
    Sprint 12 Critical Component: Circular Buffer.
    Handles high-speed data ingestion without crashing memory.
    """
    def __init__(self, size_bytes: int):
        self.size = size_bytes
        self.buffer = bytearray(size_bytes)
        self.write_ptr = 0
        self.is_full = False

    def write(self, data: bytes):
        data_len = len(data)
        if data_len > self.size:
            # Critical Case: Chunk is larger than the entire buffer
            logger.warning("[HATL] Data chunk exceeds buffer size! Overwriting everything.")
            self.buffer[:] = data[-self.size:]
            self.write_ptr = 0
            self.is_full = True
            return

        # Calculate wrap-around
        if self.write_ptr + data_len <= self.size:
            # Linear write
            self.buffer[self.write_ptr : self.write_ptr + data_len] = data
            self.write_ptr += data_len
        else:
            # Circular write (Wrap around the end)
            part1 = self.size - self.write_ptr
            part2 = data_len - part1
            self.buffer[self.write_ptr : ] = data[:part1]
            self.buffer[0 : part2] = data[part1:]
            self.write_ptr = part2
            self.is_full = True

    def dump(self) -> bytes:
        """Return correctly ordered data from the ring."""
        if not self.is_full:
            return self.buffer[:self.write_ptr]
        # If full, start reading from write_ptr (oldest data) to end, then start to write_ptr
        return self.buffer[self.write_ptr:] + self.buffer[:self.write_ptr]

class HardwareTraceEngine:
    """
    The HATL Core. 
    Orchestrates the Ring Buffer and the Protocol Decoders.
    """
    def __init__(self, arch: Architecture):
        self.arch = arch
        # 64KB Buffer (Standard for ARM CoreSight ETM on embedded)
        self.ring_buffer = RingBuffer(64 * 1024)
        self.decoded_packets: List[TracePacket] = []

    def ingest_raw_stream(self, stream_data: bytes):
        """Receive raw binary blob from hardware driver."""
        self.ring_buffer.write(stream_data)

    def process(self) -> int:
        """
        Pull data from Ring Buffer and Decode.
        Returns number of packets decoded.
        """
        raw_data = self.ring_buffer.dump()
        
        if self.arch == Architecture.INTEL_X64:
            new_packets = self._decode_intel_pt(raw_data)
        elif self.arch == Architecture.ARM_V8:
            new_packets = self._decode_arm_coresight(raw_data)
        else:
            new_packets = []

        self.decoded_packets.extend(new_packets)
        return len(new_packets)

    def _decode_intel_pt(self, data: bytes) -> List[TracePacket]:
        """
        Sprint 11: Intel PT Decoder Logic.
        Implements packet parsing for TNT and TIP.
        """
        packets = []
        i = 0
        while i < len(data):
            byte = data[i]
            
            # 1. TNT Packet (Short): Bit 0 is 0, subsequent bits are decisions
            # Signature: ends in 0 (xxxxxxx0), but not 00
            if (byte & 1) == 0 and byte != 0:
                # In real PT, we parse bits right-to-left. 
                # Simulating a "Taken" decision for the masterpiece demo logic.
                packets.append(TracePacket(type=PacketType.BRANCH_DECISION, taken=True))
                i += 1
                
            # 2. TIP Packet (Target IP): Signature 0x0D
            elif byte == 0x0D:
                if i + 8 < len(data):
                    # Unpack 64-bit Little Endian Address
                    addr = struct.unpack("<Q", data[i+1:i+9])[0]
                    packets.append(TracePacket(type=PacketType.TARGET_IP, address=addr))
                    i += 9
                else:
                    break # Stream incomplete
            
            # 3. Padding (NOP): Signature 0x00
            elif byte == 0x00:
                i += 1
            
            else:
                # Unknown packet or complex packet (FUP, MODE, etc.)
                # In a masterpiece, we skip safely rather than crashing
                i += 1
        return packets

    def _decode_arm_coresight(self, data: bytes) -> List[TracePacket]:
        """
        Sprint 12: ARM CoreSight Decoder Logic.
        """
        packets = []
        i = 0
        while i < len(data):
            byte = data[i]
            
            # Simulated ETMv4 Packet Signatures
            # 0x80 = Atom Packet (Branch)
            if byte == 0x80:
                packets.append(TracePacket(type=PacketType.BRANCH_DECISION, taken=True))
                i += 1
            # 0x01 = Overflow Warning
            elif byte == 0x01:
                packets.append(TracePacket(type=PacketType.OVERFLOW))
                logger.error("[HATL] CoreSight Buffer Overflow Marker Detected")
                i += 1
            else:
                i += 1
        return packets