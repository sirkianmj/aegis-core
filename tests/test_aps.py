from aegis.core.governance.aps import AbusePreventionSystem
import datetime

def test_security_controls():
    print("=== SPRINT 17: ABUSE PREVENTION SYSTEM TEST ===")
    
    aps = AbusePreventionSystem()
    
    # 1. Define Authorized Scope (Local Lab Only)
    allowed_network = "192.168.1.0/24"
    aps.load_scope([allowed_network])
    
    # TEST A: Valid Target
    target_good = "192.168.1.50"
    print(f"\n[TEST A] Engaging authorized target {target_good}...")
    if aps.check_engagement(target_good):
        print("[PASS] Authorized target accepted.")
    else:
        print("[FAIL] Authorized target blocked.")

    # TEST B: Unauthorized Target (The Rogue Operator Scenario)
    target_bad = "8.8.8.8"
    print(f"\n[TEST B] Engaging UNAUTHORIZED target {target_bad}...")
    if not aps.check_engagement(target_bad):
        print("[PASS] Out-of-Scope target correctly blocked.")
    else:
        print("[FAIL] CRITICAL: System allowed attack on unauthorized target!")

    # TEST C: Watermarking
    print("\n[TEST C] Verifying Forensic Watermark...")
    payload = b"\x90" * 20 # NOP Sled
    marked = aps.watermark_payload(payload)
    
    if b"__AEGIS_SIG" in marked and b"AEGIS_INSTALL" in marked:
        print(f"[PASS] Payload successfully watermarked.")
        print(f"    Raw Footer: {marked[-30:]}")
    else:
        print("[FAIL] Watermark missing.")

    # TEST D: Kill Switch (Time Travel)
    print("\n[TEST D] Simulating Heartbeat Failure...")
    # Force the clock forward 2 days
    aps.last_heartbeat = datetime.datetime.now() - datetime.timedelta(days=2)
    
    try:
        aps.check_engagement(target_good)
        print("[FAIL] System operated despite expired heartbeat!")
    except PermissionError as e:
        print(f"[PASS] System locked down: {e}")

if __name__ == "__main__":
    test_security_controls()
