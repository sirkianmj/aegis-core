from aegis.core.logic.engine import ReasoningEngine
from aegis.core.network.graph import NetworkGraph
from aegis.core.planning.planner import AttackPlanner

def test_mission_generation():
    print("=== SPRINT 3: FULL SYSTEM INTEGRATION TEST ===")
    
    # 1. Init Brain
    brain = ReasoningEngine()
    brain.load_rules()
    
    # 2. Init Map
    net = NetworkGraph()
    net.add_host("Kali", "Linux")
    net.add_host("WebSrv", "Linux")
    net.add_host("DB", "Windows", critical=True)
    
    net.add_connection("Kali", "WebSrv", 80)
    net.add_connection("WebSrv", "DB", 3306)
    
    # 3. Init Planner
    general = AttackPlanner(brain, net)
    
    # 4. Generate Plan
    plan = general.generate_plan("Kali", "DB")
    
    # 5. Review
    print(f"\n[MISSION ORDER] Target: {plan.target_ip}")
    for step in plan.steps:
        print(f"  [ ] {step}")
        
    if "EXPLOIT" in plan.steps[1]:
        print("\n[SUCCESS] AI generated a valid multi-hop attack chain.")
    else:
        print("\n[FAILURE] AI failed to plan.")

if __name__ == "__main__":
    test_mission_generation()