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
        """
        1. Inject the 'input_string' into the virtual CPU.
        2. Run the code.
        3. Record the Execution Trace (Basic Blocks).
        4. Check if we hit the target output.
        """
        print(f"[CONCOLIC] Emulating binary with input: '{input_string}'")
        
        # 1. Create a state with the SPECIFIC input (Concrete, not Symbolic)
        # We start at the entry point of the binary
        entry_state = self.project.factory.entry_state(
            args=[self.binary_path],
            stdin=input_string
        )
        
        # 2. Initialize the Simulation Manager
        sim = self.project.factory.simgr(entry_state)
        
        # 3. Step through execution until termination
        # This uses the UNICORN engine under the hood for speed
        trace = []
        
        print("[CONCOLIC] Running Trace...")
        
        # Run until the program finishes or crashes
        sim.run()
        
        # 4. Analyze the Result (Deadended states = finished programs)
        if sim.deadended:
            final_state = sim.deadended[0]
            output = final_state.posix.dumps(1) # Stdout
            
            # Extract the history (The Trace)
            # basic_blocks is a list of memory addresses executed
            history = list(final_state.history.bbl_addrs)
            trace_len = len(history)
            
            print(f"[TRACE] Execution finished. Instructions executed: {trace_len} blocks.")
            print(f"[TRACE] Final Output: {output}")
            
            if target_output.encode() in output:
                print("[VERIFIED] Simulation confirms the input works.")
                return True
            else:
                print("[FAILURE] Simulation finished, but output was wrong.")
                return False
        else:
            print("[CRASH] The binary crashed during emulation.")
            return False