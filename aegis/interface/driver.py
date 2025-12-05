from abc import ABC, abstractmethod
from typing import Dict, Any, List
from enum import Enum
from pydantic import BaseModel

class SafetyTier(Enum):
    GREEN = "GREEN"   # Read-only
    YELLOW = "YELLOW" # State-change
    RED = "RED"       # Destructive

class ScanResult(BaseModel):
    ip: str
    ports: List[int]
    os: str
    vulnerabilities: List[str]

class AegisDriver(ABC):
    """
    The Hardware Abstraction Layer (HAL).
    
    This interface ensures that the Logic Core (Brain) is completely 
    decoupled from the Network Implementation (Hands).
    """

    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to the network adapter (or simulation)."""
        pass

    @abstractmethod
    def scan_target(self, target_ip: str) -> ScanResult:
        """
        Perform a reconnaissance scan.
        In Simulation: Returns lookup data.
        In Reality: Runs Nmap/Masscan.
        """
        pass

    @abstractmethod
    def execute_payload(self, target_ip: str, payload_id: str) -> bool:
        """
        Execute an exploit payload.
        MUST reference O-SAFE checks before calling this.
        """
        pass