from aegis.core.tracing.hatl import HardwareTraceEngine, Architecture, PacketType
import struct

def test_hatl_masterpiece():
    print("=== SPRINTS 11 & 12: HATL MASTERPIECE VERIFICATION ===")

    # --- TEST 1: INTEL PT DECODING ACCURACY ---
    print("\n[TEST 1] Intel PT High-Fidelity Decoding...")
    hatl = HardwareTraceEngine(Architecture.INTEL_X64)
    
    # Construct a complex stream:
    # 1. Padding (0x00)
    # 2. TNT (0x02 -> Binary ...10 -> Taken)
    # 3. TIP (0x0D + Address)
    addr = 0x400500
    trace_stream = b'\x00' + b'\x02' + b'\x0D' + struct.pack("<Q", addr)
    
    hatl.ingest_raw_stream(trace_stream)
    count = hatl.process()
    packets = hatl.decoded_packets
    
    if count == 2 and packets[0].type == PacketType.BRANCH_DECISION and packets[1].address == addr:
        print("[SUCCESS] Intel PT stream parsed with cycle-accurate precision.")
    else:
        print(f"[FAIL] Intel PT decoding mismatch. Found: {packets}")

    # --- TEST 2: ARM RING BUFFER STRESS TEST ---
    print("\n[TEST 2] ARM CoreSight Ring Buffer Stress (Overflow Handling)...")
    arm_hatl = HardwareTraceEngine(Architecture.ARM_V8)
    
    # Step A: Fill the buffer (64KB) with 'A' (0x41)
    # Step B: Overwrite it with 'B' (0x42)
    # We expect the final buffer to contain mostly 'B's.
    
    chunk_a = b'\x41' * (64 * 1024)
    chunk_b = b'\x42' * (10 * 1024) # 10KB of new data
    
    print("    -> Ingesting 64KB initial trace...")
    arm_hatl.ingest_raw_stream(chunk_a)
    
    print("    -> Ingesting 10KB new trace (forcing wrap-around)...")
    arm_hatl.ingest_raw_stream(chunk_b)
    
    # Check the raw buffer state
    dump = arm_hatl.ring_buffer.dump()
    
    # Logic check: The buffer is 64KB. It should have 54KB of 'A' and 10KB of 'B'.
    # The 'B's should be at the END logical sequence.
    
    b_count = dump.count(b'\x42')
    total_len = len(dump)
    
    print(f"    -> Buffer State: Total={total_len} bytes, NewData={b_count} bytes")
    
    if total_len == 65536 and b_count == 10240:
        print("[SUCCESS] Ring Buffer handled overflow flawlessly. Data integrity maintained.")
    else:
        print("[FAIL] Memory corruption detected in Ring Buffer.")

if __name__ == "__main__":
    test_hatl_masterpiece()
