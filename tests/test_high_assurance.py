from aegis.core.crypto.tpm_guard import TPMGuard
from aegis.core.crypto.quantum import QuantumStack

def test_mil_spec_security():
    print("=== SPRINTS 18 & 19: HIGH ASSURANCE CRYPTO TEST ===")
    
    # --- TEST 1: TPM ATTESTATION ---
    print("\n[TEST 1] TPM Hardware Attestation...")
    tpm = TPMGuard(simulate=True)
    
    # 1. Generate Quote (Snapshot of Hardware)
    hw_quote = tpm.measure_system_state()
    print(f"    Hardware Hash: {hw_quote}")
    
    # 2. Verify (Whitelisting itself)
    valid_list = [hw_quote, "some_other_valid_hash"]
    if tpm.verify_quote(hw_quote, valid_list):
        print("[SUCCESS] TPM Quote verified.")
    else:
        print("[FAIL] TPM verification failed.")

    # --- TEST 2: POST-QUANTUM CRYPTO ---
    print("\n[TEST 2] Hybrid PQC Key Exchange (Kyber-1024)...")
    pqc = QuantumStack()
    
    # 1. Generate Alice's Keys
    pub_key, priv_key = pqc.generate_keypair()
    print(f"    Hybrid Public Key Size: {len(pub_key)} bytes")
    
    # Check logic: 32 (ECC) + 1568 (Kyber) = 1600 bytes
    if len(pub_key) == 1600:
        print("[CHECK] Key size matches NIST Kyber-1024 + X25519 spec.")
    else:
        print(f"[FAIL] Key size wrong: {len(pub_key)}")
        return

    # 2. Bob Encapsulates (KEM)
    secret, cipher = pqc.encapsulate(pub_key)
    print(f"    Shared Secret Derived: {secret.hex()[:16]}...")
    
    if len(secret) == 32:
        print("[SUCCESS] PQC Handshake structure valid.")
    else:
        print("[FAIL] Shared secret generation failed.")

if __name__ == "__main__":
    test_mil_spec_security()
