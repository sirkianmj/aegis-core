import os
from aegis.core.analysis.slicer import AngrSlicer
from aegis.core.analysis.emulator import ConcolicVerifier

def test_concolic_pipeline():
    print("=== SPRINT 8: CONCOLIC TRACE VERIFICATION ===")
    
    binary_path = os.path.abspath("targets/vuln_app")
    target_msg = "SUCCESS_ACCESS_GRANTED_LEVEL_9"

    # PART 1: SYMBOLIC DISCOVERY (The Brain)
    print("\n[STEP 1] Running Symbolic Slicer (Sprint 7)...")
    slicer = AngrSlicer(binary_path)
    # Solve for the password
    password = slicer.solve_for_output(target_msg)
    
    if not password:
        print("[FAIL] Slicer could not find password.")
        return

    # Clean null bytes
    password = password.replace('\x00', '')
    print(f"[STEP 1] Slicer found candidate: '{password}'")

    # PART 2: CONCRETE VERIFICATION (The Simulator)
    print("\n[STEP 2] Running Concolic Verifier (Sprint 8)...")
    verifier = ConcolicVerifier(binary_path)
    
    # We test if 'AegisTopSecret' actually triggers the code
    # SIMULATE KEYPRESS: We must append a newline '\n' so the C program
    # knows to null-terminate the string (converting the 'Enter' key to \0)
    success = verifier.verify_input_and_trace(password + "\n", target_msg)
    
    if success:
        print("\n[SUCCESS] Pipeline Complete. Mathematical Proof + Concrete Verification.")
    else:
        print("\n[FAILURE] The candidate password failed in simulation.")

if __name__ == "__main__":
    test_concolic_pipeline()