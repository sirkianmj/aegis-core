from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

# Import Core Engines
from aegis.core.logic.engine import ReasoningEngine
from aegis.core.logic.grammar import FactType
from aegis.core.exploitation.payload_factory import PayloadFactory
from aegis.core.governance.aps import AbusePreventionSystem

app = FastAPI(title="AEGIS Autonomous Command Interface", version="2.0.9")
# --- CORS FIX FOR UI ---
# This allows your local HTML file to talk to the Python API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow any origin (Fine for a local tool)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Systems
brain = ReasoningEngine()
brain.load_rules()
aps = AbusePreventionSystem()
# Simulate loading a scope for the demo
aps.load_scope(["10.0.0.0/8", "192.168.0.0/16", "127.0.0.1/32"])

class TargetRequest(BaseModel):
    ip: str
    os_type: str

class FeasibilityResponse(BaseModel):
    target: str
    is_vulnerable: bool
    attack_vector: str

class PayloadRequest(BaseModel):
    target_offset: int
    rip: int

@app.get("/")
def health_check():
    """Heartbeat endpoint for the dashboard."""
    return {"status": "ONLINE", "mode": "SAFE_SIMULATION", "integrity": "100%"}

@app.post("/analyze", response_model=FeasibilityResponse)
def analyze_target(req: TargetRequest):
    """
    Endpoint for SOC integration.
    Asks the Z3 Brain if a target is mathematically vulnerable.
    """
    print(f"[API] Received analysis request for {req.ip} ({req.os_type})")
    
    # 1. APS Check (Safety First)
    try:
        aps.check_engagement(req.ip)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    # 2. Logic Check
    # Simulation: If it's Linux, we assume we found an Open Port
    initial_facts = [FactType.PORT_OPEN]
    
    # Ask Z3
    possible = brain.analyze_feasibility(FactType.CREDENTIAL_FOUND, initial_facts)
    
    if possible:
        return {
            "target": req.ip,
            "is_vulnerable": True,
            "attack_vector": "PORT_OPEN -> EXPLOIT_RCE -> CREDENTIALS"
        }
    else:
        return {
            "target": req.ip,
            "is_vulnerable": False,
            "attack_vector": "NONE"
        }

@app.post("/generate-payload")
def generate_weapon(req: PayloadRequest):
    """
    Endpoint for automated weaponization.
    """
    factory = PayloadFactory()
    payload = factory.generate_buffer_overflow(req.target_offset, req.rip)
    
    if not payload:
        raise HTTPException(status_code=400, detail="Payload generation failed (Bad Chars detected)")
        
    return {"payload_hex": payload.hex(), "size": len(payload)}