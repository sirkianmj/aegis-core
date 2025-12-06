import angr
import claripy
import sys
import logging

# Silence the noisy Angr logs
logging.getLogger('angr').setLevel(logging.ERROR)

class AngrSlicer:
    """
    Tier 1 Analysis Engine.
    Uses Symbolic Execution to reverse-engineer path constraints.
    """
    def __init__(self, binary_path: str):
        self.binary_path = binary_path
        # Load the binary. auto_load_libs=False focuses analysis on OUR code, not Linux libraries.
        self.project = angr.Project(binary_path, auto_load_libs=False)

    def solve_for_output(self, target_string: str) -> str:
        """
        Find the input string required to reach a specific print output.
        """
        print(f"[SLICER] Lifting binary to Intermediate Representation (VEX)...")
        print(f"[SLICER] Hunting for state where stdout contains: '{target_string}'")

        # 1. Create the Entry State (Start at main)
        entry_state = self.project.factory.entry_state()
        
        # 2. Create a Simulation Manager (The Pathfinder)
        simulation = self.project.factory.simgr(entry_state)

        # 3. Define the "Success" Condition
        def is_successful(state):
            # Check if the target string is in the Standard Output buffer
            output = state.posix.dumps(1) # 1 = stdout
            return target_string.encode() in output

        # 4. Define the "Failure" Condition (Optimization)
        def is_failure(state):
            output = state.posix.dumps(1)
            return b"ACCESS DENIED" in output

        # 5. Run Symbolic Execution
        # explore() splits the universe into parallel universes at every 'if' statement
        simulation.explore(find=is_successful, avoid=is_failure)

        # 6. Analyze Results
        if simulation.found:
            success_state = simulation.found[0]
            # Solve the constraint: "What was in stdin (0) that caused this state?"
            solution = success_state.posix.dumps(0)
            return solution.decode(errors='ignore').strip()
        else:
            return None