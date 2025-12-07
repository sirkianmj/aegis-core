import subprocess
import json
import sys
import shutil

def test_static_security_analysis():
    print("=== SPRINT 23: SELF-SECURITY AUDIT (BANDIT) ===")
    
    # Check if bandit is installed
    if not shutil.which("bandit"):
        print("[FAIL] 'bandit' executable not found in path.")
        print("       Try running: pip install bandit")
        return

    print("[AUDIT] Running Bandit scan on 'aegis' directory...")

    # We use sys.executable to ensure we use the CURRENT environment's python
    cmd = [sys.executable, "-m", "bandit", "-r", "aegis", "-f", "json", "-lll"]
    
    try:
        # Run the subprocess
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True
        )
        
        # DEBUG BLOCK: Check if it actually ran
        if result.returncode != 0 and not result.stdout.strip():
            print(f"[FAIL] Bandit execution failed (Exit Code: {result.returncode})")
            print(f"STDERR Output:\n{result.stderr}")
            return

        # Try to parse JSON
        try:
            report = json.loads(result.stdout)
        except json.JSONDecodeError:
            print("[FAIL] Could not parse Bandit output as JSON.")
            print(f"Raw Output: '{result.stdout}'")
            print(f"Raw Errors: '{result.stderr}'")
            return
        
        # Analyze Report
        metrics = report.get('metrics', {})
        total_issues = 0
        
        # Sum up high severity issues
        for key, val in metrics.items():
            total_issues += val.get('CONFIDENCE.HIGH', 0)
            
        print(f"[AUDIT] Analysis complete. Scanned {len(metrics)} files.")
        
        if total_issues == 0:
            print("[SUCCESS] No High-Severity vulnerabilities found in AEGIS codebase.")
        else:
            print(f"[WARN] Found {total_issues} potential security issues.")
            
    except Exception as e:
        print(f"[FAIL] Audit crashed with exception: {e}")

if __name__ == "__main__":
    test_static_security_analysis()