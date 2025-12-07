import angr
import sys

class ConcolicVerifier:
    """
    Sprint 8: Concolic Execution Engine.
    Runs the binary concretely (using Unicorn) to verify symbolic solutions.
    """
    def __init__(self, binary_path: str):
        self.binary_path = binary_path
        # Force load libraries to ensure libc functions (read, strcmp) work 100% correctly
        self.project = angr.Project(binary_path, auto_load_libs=True)

    def verify_input_and_trace(self, input_string: str, target_output: str) -> bool:
        print(f"[CONCOLIC] Emulating binary with input: '{input_string}'")
        
        entry_state = self.project.factory.entry_state(args=[self.binary_path], stdin=input_string)
        sim = self.project.factory.simgr(entry_state)
        
        sim.run()
        
        # ANALYSIS 1: Did it finish normally?
        if sim.deadended:
            final_state = sim.deadended[0]
            output = final_state.posix.dumps(1)
            history = list(final_state.history.bbl_addrs)
            print(f"[TRACE] Finished. Output: {output}")
            
            if target_output.encode() in output:
                print("[VERIFIED] Simulation confirms success output.")
                return True
            return False

        # ANALYSIS 2: Did it crash? (Exploitability Index)
        if sim.errored:
            error_state = sim.errored[0].state
            # Get the Instruction Pointer (RIP/EIP) at the moment of crash
            crash_ip = error_state.solver.eval(error_state.regs.ip)
            print(f"[CRASH DETECTED] RIP at crash: {hex(crash_ip)}")
            
            # Heuristic: If RIP is a weird number (like 0x41414141), we control it.
            # 'A' = 0x41. If we see 0x4141..., we overwrote the pointer.
            if crash_ip == 0x4141414141414141 or (crash_ip >> 32) == 0x41414141:
                print("[TRIAGE] CRITICAL: Instruction Pointer Overwritten by User Input!")
                print("[TRIAGE] Exploitability Index: 10/10 (High)")
                return True # A controlled crash is a SUCCESS for an exploit tool
            else:
                print("[TRIAGE] Crash is likely a SEGFAULT (Index: 2/10).")
                return False
                
        return False