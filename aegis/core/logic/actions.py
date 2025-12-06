from typing import List, Optional
from pydantic import BaseModel
from .grammar import FactType, AccessLevel, AssetType

class CyberAction(BaseModel):
    """
    Represents a discrete step in an attack graph.
    The AI uses these as building blocks to construct a path.
    """
    id: str
    name: str
    description: str
    safety_tier: str  # GREEN, YELLOW, RED
    
    # Prerequisite: What must be TRUE for this action to be valid?
    # Example: To run 'Exploit', 'PORT_OPEN' and 'VULN_PRESENT' must be true.
    preconditions: List[FactType]
    
    # Effect: What becomes TRUE after this action succeeds?
    # Example: After 'Exploit', 'USER_SHELL' becomes true.
    postconditions: List[FactType]
    
    # Cost: How 'loud' or resource-intensive is this? (0-100)
    # The AI optimizes for the lowest cost (stealth).
    cost: int = 10

# --- THE STANDARD LIBRARY OF WARFARE ---
# These are the rules the AI is allowed to use.

# 1. Reconnaissance (Safe / GREEN)
SCAN_PORT = CyberAction(
    id="ACT_SCAN_TCP",
    name="TCP Connect Scan",
    description="Identify open ports via TCP handshake",
    safety_tier="GREEN",
    preconditions=[],  # Can always try to scan
    postconditions=[FactType.PORT_OPEN],
    cost=1
)

identify_service = CyberAction(
    id="ACT_ID_SERVICE",
    name="Service Version Detection",
    description="Grab banner and fingerprint service",
    safety_tier="GREEN",
    preconditions=[FactType.PORT_OPEN],
    postconditions=[FactType.SERVICE_VERSION],
    cost=5
)

# 2. Vulnerability Analysis (Safe / GREEN)
check_vuln = CyberAction(
    id="ACT_CHECK_VULN",
    name="Vulnerability Verification",
    description="Check service version against CVE database",
    safety_tier="GREEN",
    preconditions=[FactType.SERVICE_VERSION],
    postconditions=[FactType.VULNERABILITY_PRESENT],
    cost=2
)

# 3. Exploitation (Dangerous / RED)
exploit_rce = CyberAction(
    id="ACT_EXPLOIT_RCE",
    name="Remote Code Execution",
    description="Launch buffer overflow payload to gain shell",
    safety_tier="RED",  # <--- GOVERNANCE ENGINE WILL FLAG THIS
    preconditions=[FactType.PORT_OPEN, FactType.VULNERABILITY_PRESENT],
    postconditions=[FactType.CREDENTIAL_FOUND], # Simplified for Sprint 1
    cost=90
)

# The "Grimoire" (List of all known spells)
ALL_ACTIONS = [SCAN_PORT, identify_service, check_vuln, exploit_rce]