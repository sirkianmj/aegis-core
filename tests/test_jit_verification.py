from aegis.core.logic.uncertainty import UncertainBool, TruthState
import random

def mock_network_probe():
    """Simulates sending a TCP SYN packet to check a port."""
    print("    <PHYSICAL LAYER> Sending TCP SYN to 192.168.1.5:80...")
    # Simulate that the port is actually OPEN
    return True

def test_jit_logic():
    print("=== SPRINT 5: JIT VERIFICATION TEST ===")
    
    # 1. Initialize a Fact (Port 80 is maybe open?)
    is_port_open = UncertainBool(TruthState.UNCERTAIN, confidence=0.5)
    
    # 2. Attach the physical sensor
    is_port_open.set_probe(mock_network_probe)
    
    print(f"State before check: {is_port_open.state.name}")
    
    # 3. The Logic Engine asks: "Is the port open?"
    # This triggers the __bool__ method, which calls .collapse()
    if is_port_open:
        print("[LOGIC] Port confirmed open! Proceeding with attack.")
    else:
        print("[LOGIC] Port closed. Aborting.")
        
    print(f"State after check:  {is_port_open.state.name}")
    
    # 4. Check again (Should NOT probe twice, because it's now cached)
    print("\n[RE-CHECK] Asking again...")
    if is_port_open:
        print("[LOGIC] Still open (Loaded from Cache).")

if __name__ == "__main__":
    test_jit_logic()