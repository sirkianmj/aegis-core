import os
import time
from aegis.core.analysis.slicer import AngrSlicer

def test_symbolic_execution():
    print("=== SPRINT 7: CONCRETE BINARY ANALYSIS ===")
    
    # 1. Locate the binary
    binary_path = os.path.abspath("targets/vuln_app")
    if not os.path.exists(binary_path):
        print(f"[ERROR] Binary {binary_path} missing! Did you run gcc?")
        return

    # 2. Initialize the Engine
    print(f"[TARGET] {binary_path}")
    slicer = AngrSlicer(binary_path)
    
    # 3. Define the Goal
    # We want to force the program to print the success message
    target_output = "SUCCESS_ACCESS_GRANTED_LEVEL_9"
    
    start_time = time.time()
    
    # 4. EXECUTE ANALYSIS (This is the heavy lifting)
    result = slicer.solve_for_output(target_output)
    if result: result = result.replace('\x00', '') # Clean up memory padding
    
    duration = time.time() - start_time
    
    # 5. Verify Result
    if result:
        print(f"\n[SUCCESS] Constraint Solved in {duration:.2f} seconds!")
        print(f"    mathematical_solution = '{result}'")
        
        if result == "AegisTopSecret":
            print("[VERIFIED] The solution matches the hardcoded C password.")
        else:
            print("[WARNING] Solved, but result is unexpected.")
    else:
        print("\n[FAILURE] Analysis timed out or path not found.")

if __name__ == "__main__":
    test_symbolic_execution()