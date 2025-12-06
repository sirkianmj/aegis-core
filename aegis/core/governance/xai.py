import json
import datetime
from typing import List, Dict, Any
from pydantic import BaseModel

class DecisionNode(BaseModel):
    timestamp: str
    decision_type: str  # e.g., "PLANNING", "SAFETY", "EXECUTION"
    input_data: str
    outcome: str
    reasoning: str
    confidence: float

class XAIEngine:
    """
    The 'Black Box' Flight Recorder.
    Ensures every automated action is traceable to a logic rule.
    """
    def __init__(self):
        self.trace_log: List[DecisionNode] = []

    def log_decision(self, type: str, input: str, outcome: str, reason: str, confidence: float = 1.0):
        """Record a thought process."""
        entry = DecisionNode(
            timestamp=datetime.datetime.now().isoformat(),
            decision_type=type,
            input_data=input,
            outcome=outcome,
            reasoning=reason,
            confidence=confidence
        )
        self.trace_log.append(entry)
        # In a real app, this would write to a tamper-proof database
        print(f"[XAI AUDIT] {type}: {outcome} | Because: {reason}")

    def generate_proof_report(self) -> str:
        """Export the full thought process as a JSON audit trail."""
        return json.dumps([entry.model_dump() for entry in self.trace_log], indent=2)