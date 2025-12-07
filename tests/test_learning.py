from aegis.core.learning.cle import ContinuousLearningEngine
from aegis.core.governance.xai import DecisionNode
import datetime

def test_machine_learning():
    print("=== SPRINT 15: CONTINUOUS LEARNING TEST ===")
    
    cle = ContinuousLearningEngine()
    
    # 1. Generate Synthetic Training Data
    # Scenario: "Exploit A" fails consistently on "Linux 5.15"
    logs = []
    
    # Add 3 failures
    for i in range(3):
        logs.append(DecisionNode(
            timestamp=datetime.datetime.now().isoformat(),
            decision_type="EXECUTION",
            input_data="Payload: CVE-2021-41773 | TargetOS: Linux 5.15",
            outcome="FAILED",
            reasoning="Connection Reset",
            confidence=1.0
        ))
        
    # Add 1 success (Control group - different OS)
    logs.append(DecisionNode(
        timestamp=datetime.datetime.now().isoformat(),
        decision_type="EXECUTION",
        input_data="Payload: CVE-2021-41773 | TargetOS: Linux 4.4",
        outcome="SUCCESS",
        reasoning="Shell spawned",
        confidence=1.0
    ))

    # 2. Trigger Learning
    cle.ingest_logs(logs)
    
    # 3. Verify Knowledge Acquisition
    rules = cle.get_avoidance_constraints()
    
    if len(rules) > 0:
        print(f"\n[SUCCESS] CLE deduced {len(rules)} new rules.")
        print(f"    Rule 1: {rules[0]}")
        
        if "Linux 5.15" in rules[0] and "AVOID" in rules[0]:
            print("[VERIFIED] Logic correctly identified the incompatible feature.")
    else:
        print("\n[FAIL] CLE failed to learn from mistakes.")

if __name__ == "__main__":
    test_machine_learning()
