from typing import List, Dict, Optional
from aegis.core.governance.xai import XAIEngine, DecisionNode
from aegis.core.logic.grammar import FactType

class LearnedRule:
    """Represents a rule deduced from observation."""
    def __init__(self, action_id: str, condition: str, confidence: float):
        self.action_id = action_id
        self.condition = condition # e.g., "OS_VERSION=5.15"
        self.confidence = confidence # 0.0 to 1.0

    def __repr__(self):
        return f"IF {self.condition} THEN AVOID {self.action_id} (Conf: {self.confidence:.2f})"

class ContinuousLearningEngine:
    """
    Sprint 15: Inductive Logic Programming (ILP) implementation.
    Parses execution logs to find correlations between Features and Failures.
    """
    def __init__(self):
        self.rules: List[LearnedRule] = []
        
    def ingest_logs(self, logs: List[DecisionNode]):
        """
        The Learning Step.
        Look for actions that failed and what the target looked like.
        """
        print(f"[CLE] Analyzing {len(logs)} operational events for patterns...")
        
        failures = [x for x in logs if x.outcome == "FAILED"]
        
        # Simple ILP: Frequency Counting
        # Map (Action, Condition) -> Failure Count
        correlation_map: Dict[str, int] = {}
        
        for fail in failures:
            # Parse the input data to extract features (Mock parsing for v2.0.9)
            # Input format: "Payload: CVE-2021-41773 | TargetOS: Linux 5.15"
            if "|" in fail.input_data:
                parts = fail.input_data.split("|")
                action = parts[0].strip()
                feature = parts[1].strip()
                
                key = f"{action}::{feature}"
                correlation_map[key] = correlation_map.get(key, 0) + 1

        # Inductive Step: If failures > threshold, create a Rule
        for key, count in correlation_map.items():
            if count >= 3: # If it failed 3 times, it's a pattern
                action, feature = key.split("::")
                # Calculate confidence (simplified)
                confidence = min(count * 0.2, 0.99)
                
                new_rule = LearnedRule(action, feature, confidence)
                self.rules.append(new_rule)
                print(f"[CLE] 🧠 NEW KNOWLEDGE ACQUIRED: {new_rule}")

    def get_avoidance_constraints(self) -> List[str]:
        """Export rules back to the Planner/Z3."""
        return [str(r) for r in self.rules]