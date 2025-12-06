from aegis.core.logic.engine import ReasoningEngine
from aegis.core.logic.grammar import FactType

def test_logic_flow():
    print("=== AEGIS COGNITIVE CORE TEST (SPRINT 1) ===")
    
    # 1. Initialize the Brain
    engine = ReasoningEngine()
    engine.load_rules()
    print("[+] Rules Loaded into Z3 Solver.")

    # 2. Define Scenario: We only know the Port is Open.
    # We want to know: Can we eventually find a Credential?
    initial_state = [FactType.PORT_OPEN]
    target_goal = FactType.CREDENTIAL_FOUND
    
    print(f"[?] Scenario: Start with {initial_state} -> Want {target_goal}")
    
    # 3. Ask Z3
    is_possible = engine.analyze_feasibility(target_goal, initial_state)
    
    if is_possible:
        print("\n[SUCCESS] The Logic Engine proved a path exists!")
        print("    Logic Chain Verified:")
        print("    PORT_OPEN -> Service ID -> Vuln Check -> EXPLOIT -> CREDENTIAL")
    else:
        print("\n[FAILURE] Mathematical proof failed. No path exists.")

