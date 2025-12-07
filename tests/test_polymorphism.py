from aegis.core.exploitation.obfuscator import PolymorphicFactory
import hashlib
import os

def get_file_hash(filepath):
    with open(filepath, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def test_signature_evasion():
    print("=== SPRINT 16: POLYMORPHIC ENGINE TEST ===")
    
    factory = PolymorphicFactory()
    
    # Dummy Shellcode (NOP sled)
    shellcode = b"\x90" * 32
    
    # 1. Generate First Mutant
    print("\n[GEN 1] Creating Mutant Alpha...")
    bin1 = factory.generate_loader(shellcode, "mutant_alpha")
    if not bin1: return
    
    # 2. Generate Second Mutant
    print("\n[GEN 2] Creating Mutant Beta...")
    bin2 = factory.generate_loader(shellcode, "mutant_beta")
    if not bin2: return
    
    # 3. Compare Signatures
    hash1 = get_file_hash(bin1)
    hash2 = get_file_hash(bin2)
    
    print(f"\n[ANALYSIS] Mutant Alpha Hash: {hash1[:16]}...")
    print(f"[ANALYSIS] Mutant Beta  Hash: {hash2[:16]}...")
    
    if hash1 != hash2:
        print("\n[SUCCESS] Polymorphism Verified. Signatures are unique.")
        print("    Antivirus logic (Signature Matching) defeated.")
    else:
        print("\n[FAIL] Binaries are identical. Polymorphism failed.")

if __name__ == "__main__":
    test_signature_evasion()
