from aegis.core.governance.policy import OSafePolicy, SafetyViolation
from aegis.core.logic.actions import exploit_rce, SCAN_PORT
from aegis.core.network.graph import NetworkNode

def test_governance():
    print("=== SPRINT 4: SAFETY PROTOCOL TEST ===")
    
    # 1. Define Targets
    boring_server = NetworkNode(ip="1.2.3.4", hostname="DevServer", os="Linux", is_critical=False)
    crown_jewels = NetworkNode(ip="9.9.9.9", hostname="Production_DB", os="Windows", is_critical=True)
    
    # 2. Test GREEN Action (Scanning) - Should Pass on Both
    print("\n[TEST 1] Scanning Critical Asset...")
    try:
        OSafePolicy.enforce(SCAN_PORT, crown_jewels)
        print("[PASS] Scanning allowed.")
    except SafetyViolation:
        print("[FAIL] Scanning was blocked!")

    # 3. Test RED Action on Low Value Target - Should Pass
    print("\n[TEST 2] Exploiting Dev Server...")
    try:
        OSafePolicy.enforce(exploit_rce, boring_server)
        print("[PASS] Exploitation allowed on non-critical target.")
    except SafetyViolation:
        print("[FAIL] Exploit blocked unnecessarily.")

    # 4. Test RED Action on CRITICAL Target - MUST FAIL
    print("\n[TEST 3] Exploiting PRODUCTION DATABASE...")
    try:
        OSafePolicy.enforce(exploit_rce, crown_jewels)
        print("[FAIL] SAFETY FAILURE! AI destroyed production!")
    except SafetyViolation as e:
        print(f"[PASS] Governance correctly blocked the attack:\n       {e}")

if __name__ == "__main__":
    test_governance()