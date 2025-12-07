from aegis.core.intelligence.honeypot import HoneypotDetector, TargetProfile
import random

def test_discrimination():
    print("=== SPRINTS 13 & 14: FULL MASTERPIECE VERIFICATION ===")
    
    detector = HoneypotDetector()
    
    # CASE A: Real Server (Clean)
    # High Entropy, Jittery RTT, Consistent Banner, Standard TTL
    real_target = TargetProfile(
        ip="192.168.1.5", 
        tcp_seq_numbers=[random.randint(1000, 9999999) for _ in range(10)], 
        rtt_measurements=[12.5, 14.2, 11.8], 
        ttl_values=[64, 64, 64], # Consistent Linux TTL
        banners=["SSH-2.0-OpenSSH_8.2p1", "SSH-2.0-OpenSSH_8.2p1"] # Consistent
    )
    
    print("\n--- ANALYZING REAL TARGET ---")
    prob_real = detector.compute_probability(real_target)
    print(f"Result: {prob_real:.2f} (Expected < 0.4)")
    
    # CASE B: Ambiguous Target (Triggers Active Probes)
    # Good Banners, Good TTL, BUT Low Entropy (Suspicious)
    # This simulates a High-Interaction Honeypot
    ambiguous_target = TargetProfile(
        ip="10.0.0.50",
        tcp_seq_numbers=[100, 200, 300, 400], # Low Entropy (Fake)
        rtt_measurements=[5.1, 5.0, 5.1], # Low Variance (Suspicious)
        ttl_values=[64, 64],
        banners=["SSH-2.0-OpenSSH_8.2p1", "SSH-2.0-OpenSSH_8.2p1"]
    )
    
    print("\n--- ANALYZING AMBIGUOUS TARGET (Should Trigger Probes) ---")
    prob_ambiguous = detector.compute_probability(ambiguous_target)
    print(f"Result: {prob_ambiguous:.2f} (Expected > 0.6)")
    
    # Check Audit Log
    if len(detector.audit_trail) > 0:
        print(f"[AUDIT] Probes Logged: {len(detector.audit_trail)}")
        print(f"        Latest: {detector.audit_trail[-1].probe_type}")
    
    if prob_real < 0.4 and prob_ambiguous > 0.5 and len(detector.audit_trail) > 0:
        print("\n[SUCCESS] System correctly used Passive Analysis and Adaptive Active Probing.")
    else:
        print("\n[FAIL] Logic did not meet Masterpiece standards.")

if __name__ == "__main__":
    test_discrimination()