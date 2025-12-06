from aegis.core.governance.xai import XAIEngine

def test_explainability():
    print("=== SPRINT 6: XAI COMPLIANCE TEST ===")
    
    # 1. Initialize Recorder
    recorder = XAIEngine()
    
    # 2. Simulate a Decision Chain
    # Step A: Scan
    recorder.log_decision(
        type="PLANNING",
        input="Target 192.168.1.5",
        outcome="SELECTED_SCAN",
        reason="Target is unknown. Reconnaissance required.",
        confidence=1.0
    )
    
    # Step B: Safety Check
    recorder.log_decision(
        type="SAFETY",
        input="Action: EXPLOIT_RCE",
        outcome="APPROVED",
        reason="Target is NOT critical. O-SAFE Policy Rule #3 passed.",
        confidence=1.0
    )
    
    # Step C: Execution Failure (JIT)
    recorder.log_decision(
        type="EXECUTION",
        input="Payload: CVE-2021-41773",
        outcome="FAILED",
        reason="JIT Probe detected patch installed.",
        confidence=0.9
    )
    
    # 3. Generate the Audit Report
    print("\n[GENERATING LEGAL AUDIT TRAIL]...")
    report = recorder.generate_proof_report()
    
    # 4. Verify the JSON
    if "O-SAFE Policy Rule #3" in report:
        print("[SUCCESS] Audit trail contains specific reasoning logic.")
        print("Preview of Report:")
        print(report)
    else:
        print("[FAILURE] Report missing reasoning details.")

if __name__ == "__main__":
    test_explainability()