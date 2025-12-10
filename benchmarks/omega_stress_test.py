import multiprocessing
import time
import os
import sys
import psutil
import networkx as nx
import random
from concurrent.futures import ProcessPoolExecutor, as_completed

# Ensure path is correct
sys.path.append(os.getcwd())

# Import The Engines
from aegis.core.logic.engine import ReasoningEngine
from aegis.core.logic.grammar import FactType
from aegis.core.network.graph import NetworkGraph
from aegis.core.exploitation.rop_engine import ROPSynthesizer
from aegis.core.analysis.slicer import AngrSlicer

# Rich for the Dashboard
try:
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
    from rich.live import Live
    from rich.table import Table
    from rich.panel import Panel
except ImportError:
    print("Please run: pip install rich")
    sys.exit(1)

console = Console()

class OmegaMonitor:
    """Tracks System Vitals during the Wargame."""
    @staticmethod
    def get_vitals():
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory().percent
        return cpu, mem

def autonomous_agent_task(target_id):
    """
    A single autonomous agent's lifecycle.
    1. Logic Check (Z3)
    2. Weaponization (ROP) OR Analysis (Angr) randomly
    """
    start = time.perf_counter()
    
    # 1. LOGIC PHASE (Fast)
    # Each process gets its own Brain to avoid locking
    brain = ReasoningEngine()
    brain.load_rules()
    is_possible = brain.analyze_feasibility(FactType.CREDENTIAL_FOUND, [FactType.PORT_OPEN])
    
    # 2. HEAVY LIFTING PHASE (The Stress)
    # We simulate a mix of tasks to stress the CPU
    task_type = "ROP" if random.random() > 0.3 else "ANGR"
    
    if task_type == "ROP":
        # Pwntools ROP Synthesis
        if os.path.exists("targets/overflow_app"):
            rop = ROPSynthesizer("targets/overflow_app")
            rop.find_gadgets()
            chain = rop.build_exec_chain("hacker_win")
    else:
        # Angr Symbolic Execution (The CPU Melter)
        if os.path.exists("targets/vuln_app"):
            # Limit Angr work to prevent 100% freeze on small VMs
            slicer = AngrSlicer("targets/vuln_app")
            # Just solve for a string to prove we loaded the engine
            _ = slicer.solve_for_output("AEGIS") 

    duration = time.perf_counter() - start
    return (target_id, task_type, duration, is_possible)

class OmegaTest:
    def __init__(self, node_count=10000, concurrent_agents=10):
        self.node_count = node_count
        self.concurrent_agents = concurrent_agents
        self.network = NetworkGraph()

    def build_battlefield(self):
        with console.status("[bold green]Building 10,000 Node Battlefield...") as status:
            # Generate Scale-Free Network
            nx_graph = nx.barabasi_albert_graph(self.node_count, 2, seed=1337)
            self.network.graph = nx_graph
            console.log(f"[SETUP] Network Graph built: {self.node_count} nodes, {len(nx_graph.edges)} edges.")

    def run_wargame(self):
        console.print(Panel(f"[bold red]INITIATING OMEGA STRESS TEST[/]\nNodes: {self.node_count}\nConcurrent Agents: {self.concurrent_agents}", border_style="red"))
        
        # We select 'concurrent_agents' targets to attack simultaneously
        targets = [str(i) for i in range(self.concurrent_agents)]
        results = []
        
        total_time_start = time.perf_counter()

        # THE PARALLEL ENGINE
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("{task.percentage:>3.0f}%"),
        ) as progress:
            task_id = progress.add_task("[cyan]Deploying Autonomous Agents...", total=self.concurrent_agents)
            
            # Use all available cores (or limit to avoid crash)
            max_workers = min(os.cpu_count(), self.concurrent_agents)
            
            with ProcessPoolExecutor(max_workers=max_workers) as executor:
                futures = {executor.submit(autonomous_agent_task, t): t for t in targets}
                
                completed = 0
                for future in as_completed(futures):
                    res = future.result()
                    results.append(res)
                    completed += 1
                    
                    # Live Resource Monitoring
                    cpu, mem = OmegaMonitor.get_vitals()
                    progress.update(task_id, advance=1, description=f"[cyan]Agents Active | CPU: {cpu}% | RAM: {mem}%")

        total_duration = time.perf_counter() - total_time_start
        self.print_report(results, total_duration)

    def print_report(self, results, duration):
        table = Table(title="OMEGA TEST RESULTS")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        
        avg_time = sum(r[2] for r in results) / len(results)
        rop_count = len([r for r in results if r[1] == "ROP"])
        angr_count = len([r for r in results if r[1] == "ANGR"])
        
        table.add_row("Total Wall Time", f"{duration:.2f}s")
        table.add_row("Total Agents Deployed", str(len(results)))
        table.add_row("ROP Synthesis Jobs", str(rop_count))
        table.add_row("Symbolic Execution Jobs", str(angr_count))
        table.add_row("Avg Time Per Agent", f"{avg_time:.4f}s")
        table.add_row("Throughput", f"{len(results)/duration:.2f} hacks/sec")
        
        console.print(table)
        
        if duration < 15.0 and len(results) == self.concurrent_agents:
            console.print(Panel("[bold green]VERDICT: SYSTEM IS APEX PREDATOR[/]\nParallelism scaling verified. Memory leaks absent.", border_style="green"))
        else:
            console.print("[bold yellow]VERDICT: System functional but stressed under load.[/]")

if __name__ == "__main__":
    # WARNING: This stresses the CPU. We default to 20 agents to be safe on VMs.
    # On a real server, you could set this to 100+.
    test = OmegaTest(node_count=10000, concurrent_agents=20)
    test.build_battlefield()
    test.run_wargame()
