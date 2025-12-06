from enum import Enum, auto
from typing import List, Optional
from pydantic import BaseModel, Field

class AssetType(Enum):
    SERVER = "server"
    WORKSTATION = "workstation"
    DATABASE = "database"
    ROUTER = "router"

class AccessLevel(Enum):
    NONE = 0
    NETWORK_ACCESS = 1
    USER_SHELL = 2
    ROOT_SYSTEM = 3
    DOMAIN_ADMIN = 4

class FactType(Enum):
    PORT_OPEN = "PORT_OPEN"
    SERVICE_VERSION = "SERVICE_VERSION"
    VULNERABILITY_PRESENT = "VULN_PRESENT"
    CREDENTIAL_FOUND = "CRED_FOUND"
    FILE_FOUND = "FILE_FOUND"

class Fact(BaseModel):
    """
    A 'Fact' is a single unit of truth in the Z3 universe.
    Example: Fact(type=PORT_OPEN, target="192.168.1.5", details="80/tcp")
    """
    type: FactType
    target: str
    details: str
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)

class AttackStep(BaseModel):
    """
    An Abstract Action in the Grammar.
    Safety Tier is critical here (Green/Yellow/Red).
    """
    name: str
    description: str
    safety_tier: str  # GREEN, YELLOW, RED
    
    # What must be true BEFORE this step runs?
    preconditions: List[FactType]
    
    # What becomes true AFTER this step runs?
    postconditions: List[FactType]