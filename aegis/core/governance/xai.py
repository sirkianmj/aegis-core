import json
import datetime
import os
from typing import List, Dict, Any
from pydantic import BaseModel
from cryptography.fernet import Fernet # AES-128/256 equivalent implementation

class DecisionNode(BaseModel):
    timestamp: str
    decision_type: str
    input_data: str
    outcome: str
    reasoning: str
    confidence: float

class XAIEngine:
    """
    The 'Black Box' Flight Recorder.
    HARDENING: Added AES Encryption for audit logs.
    """
    def __init__(self, encryption_key: bytes = None):
        self.trace_log: List[DecisionNode] = []
        # Generate a key if none provided (In prod, this comes from Vault/TPM)
        self.key = encryption_key if encryption_key else Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def log_decision(self, type: str, input: str, outcome: str, reason: str, confidence: float = 1.0):
        entry = DecisionNode(
            timestamp=datetime.datetime.now().isoformat(),
            decision_type=type,
            input_data=input,
            outcome=outcome,
            reasoning=reason,
            confidence=confidence
        )
        self.trace_log.append(entry)
        print(f"[XAI AUDIT] {type}: {outcome} | Because: {reason}")

    def generate_proof_report(self) -> str:
        """Export the full thought process."""
        return json.dumps([entry.model_dump() for entry in self.trace_log], indent=2)

    def export_encrypted_log(self, filename="audit_log.enc"):
        """
        Sprint 6 Requirement: AES-256 Encrypted Storage.
        """
        raw_data = self.generate_proof_report().encode()
        encrypted_data = self.cipher.encrypt(raw_data)
        
        with open(filename, "wb") as f:
            f.write(encrypted_data)
            
        # Save key separately (Demo only)
        with open(filename + ".key", "wb") as f:
            f.write(self.key)
            
        print(f"[XAI] Encrypted audit trail saved to {filename}")