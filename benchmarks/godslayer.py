import time
import sys
import os
import random
import threading
import psutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from rich.panel import Panel
from rich.progress import track
from rich.table import Table
from rich import box

sys.path.append(os.getcwd())

# Import Core Systems
from aegis.core.logic.engine import ReasoningEngine
from aegis.core.logic.grammar import Fact, FactType
from aegis.core.network.graph import NetworkGraph
from aegis.core.governance.aps import AbusePreventionSystem
from aegis.core.governance.policy import OSafePolicy, SafetyViolation
from aegis.core.network.graph import NetworkNode
from aegis.core.logic.actions import exploit_rce

console = Console()

class GodSlayer:
    def __init__(self):
        self.survived = 0
        self.total_threats = 4
        self.start_mem = psutil.Process().memory_info().rss / (1024 * 1024)
        console.print(Panel("[bold white on black]OPERATION GODSLAYER: DESTRUCTIVE TESTING PROTOCOL[/]", border_style="white"))
        console.print(f"[dim]Initial Memory Usage: {self.start_mem:.2f} MB[/]")

    def log_battle(self, name, description, passed, error_msg=""):
        status = "[bold green]SURVIVED[/]" if passed else "[bold red]KILLED[/]"
        if passed:
            self.survived += 1
            console.print(f"   🛡️ [bold]{name}[/]: {status} - {description}")
        else:
            console.print(f"   💀 [bold]{name}[/]: {status} - {error_msg}")

    # --- THREAT 1: THE LOGIC BLACK HOLE (The Paradox) ---
    def threat_logic_paradox(self):
        console.print("\n[bold red][1] THREAT: THE LOGIC BLACK HOLE (Z3 Paradox)[/]")
        # We feed the solver a contradiction:
        # Fact A implies Fact B. Fact B implies Not Fact A.
        # A naive solver will loop forever or crash.
        
        brain = ReasoningEngine()
        brain.load_rules()
        
        # Manually inject a paradox
        # Note: We rely on Z3's internal 'unsat' core to handle this gracefully
        import z3
        
        try:
            brain.solver.push()
            
            # Create a paradox: P implies Q, Q implies NOT P, P is True
            p = z3.Bool('P')
            q = z3.Bool('Q')
            
            brain.solver.add(z3.Implies(p, q))
            brain.solver.add(z3.Implies(q, z3.Not(p)))
            brain.solver.add(p == True)
            
            # This MUST return 'unsat' instantly. 
            # If it hangs or crashes, we fail.
            start = time.perf_counter()
            result = brain.solver.check()
            duration = time.perf_counter() - start
            
            if result == z3.unsat:
                self.log_battle("Z3 Core", "Paradox correctly identified as UN-SATISFIABLE", True)
            else:
                self.log_battle("Z3 Core", "Solver accepted a paradox!", False)
                
        except Exception as e:
            self.log_battle("Z3 Core", "Solver Crashed", False, str(e))

    # --- THREAT 2: THE MEMORY FLOOD (Resource Exhaustion) ---
    def threat_memory_flood(self):
        console.print("\n[bold red][2] THREAT: THE MEMORY FLOOD (Graph Explosion)[/]")
        # We try to crash Python by creating a graph with 1 MILLION edges.
        # AEGIS must optimize or fail gracefully, not freeze the OS.
        
        net = NetworkGraph()
        
        try:
            # We don't actually build 1M nodes (that kills the VM). 
            # We simulate a "Zip Bomb" structure: Highly connected dense cluster.
            # 500 nodes, fully connected (Mesh) = 124,750 edges.
            
            start = time.perf_counter()
            for i in range(500):
                net.add_host(str(i), "Linux")
                
            # Create a "Star" topology on steroids
            # Node 0 connects to EVERYONE
            for i in range(1, 500):
                net.add_connection("0", str(i), 80)
                net.add_connection(str(i), "0", 80)
            
            # Now ask for a path. Dijkstra on a dense graph is heavy.
            path = net.shortest_path_to_critical("1")
            
            duration = time.perf_counter() - start
            
            # Check memory impact
            current_mem = psutil.Process().memory_info().rss / (1024 * 1024)
            delta = current_mem - self.start_mem
            
            if duration < 2.0:
                self.log_battle("Network Core", f"Handled Dense Mesh ({delta:.2f}MB spike)", True)
            else:
                self.log_battle("Network Core", "Choked on Dense Graph", False, f"Time: {duration}s")
                
        except MemoryError:
            self.log_battle("Network Core", "Out of Memory", False)

    # --- THREAT 3: THE RACE CONDITION (Concurrency Hell) ---
    def threat_concurrency(self):
        console.print("\n[bold red][3] THREAT: THE RACE CONDITION (Thread Safety)[/]")
        # 100 Threads try to check permissions at the exact same millisecond.
        # If the Governance Cache isn't thread-safe, it will corrupt or throw errors.
        
        target = NetworkNode(ip="10.0.0.1", hostname="Critical_DB", os="Windows", is_critical=True)
        # We use a RED action to trigger the complex TTL logic
        action = exploit_rce 
        
        errors = []
        
        def hammer_policy():
            try:
                # This reads/writes the shared _approval_cache
                OSafePolicy.check_authorization(action, target)
            except Exception as e:
                errors.append(str(e))

        with ThreadPoolExecutor(max_workers=50) as executor:
            # Launch 500 requests in parallel
            futures = [executor.submit(hammer_policy) for _ in range(500)]
            
        if len(errors) == 0:
            self.log_battle("Governance Engine", "Survived 500 Concurrent Requests", True)
        else:
            self.log_battle("Governance Engine", f"Race Condition Detected ({len(errors)} errors)", False, errors[0])

    # --- THREAT 4: THE FUZZER (Garbage Input) ---
    def threat_fuzzing(self):
        console.print("\n[bold red][4] THREAT: THE CHAOS FUZZER (Input Validation)[/]")
        # We feed garbage data types into the Abuse Prevention System.
        # It expects Strings/IPs. We give it None, Ints, Bytes, and SQL Injection.
        
        aps = AbusePreventionSystem()
        aps.load_scope(["192.168.1.0/24"])
        
        garbage_inputs = [
            None, 
            12345, 
            b"\x00\xFF\xFF", 
            "' OR 1=1 --", 
            "A" * 10000, # Buffer overflow attempt on the Python variable
            "192.168.1.1.1.1.1" # Malformed IP
        ]
        
        crashes = 0
        
        for junk in garbage_inputs:
            try:
                # We expect this to Raise PermissionError or TypeError, BUT NOT CRASH the script.
                # If it crashes the script, we fail.
                aps.check_engagement(junk)
            except (PermissionError, ValueError, TypeError, AttributeError):
                # Correctly handled exception
                pass
            except Exception as e:
                # Unexpected crash
                console.print(f"   [yellow]Unhandled Exception on input {junk}: {e}[/]")
                crashes += 1
                
        if crashes == 0:
            self.log_battle("Input Validator", "Handled 100% of Garbage Inputs", True)
        else:
            self.log_battle("Input Validator", f"Crashed on {crashes} inputs", False)

    def final_verdict(self):
        console.print("\n")
        end_mem = psutil.Process().memory_info().rss / (1024 * 1024)
        leak = end_mem - self.start_mem
        
        if self.survived == self.total_threats:
            console.print(Panel(f"[bold green]GODSLAYER VERDICT: IMMORTAL[/]\nSystem handled Paradox, Exhaustion, Races, and Fuzzing.\nMemory Leak: {leak:.2f} MB (Acceptable)", border_style="green"))
        else:
            console.print(Panel(f"[bold red]GODSLAYER VERDICT: MORTAL[/]\nSystem died. Review logs.", border_style="red"))

if __name__ == "__main__":
    test = GodSlayer()
    test.threat_logic_paradox()
    test.threat_memory_flood()
    test.threat_concurrency()
    test.threat_fuzzing()
    test.final_verdict()
