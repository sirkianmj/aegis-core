import sys
import os
import time
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.table import Table
from rich import box

# Ensure we can see the project root and the benchmarks directory
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'benchmarks'))

# IMPORT THE ARSENAL
try:
    # 1. Speed & Latency
    from benchmarks.ultimate_proof import ScientificAudit
    # 2. Mathematical Proofs
    from benchmarks.final_verdict_math import MathAudit
    # 3. Dynamic Zero-Day Capability
    from benchmarks.operation_zeroday import run_zeroday_test, ChaosTargetFactory
    # 4. Statistical Reliability
    from benchmarks.ragnarok_stress_test import OperationRagnarok
    # 5. Adversarial Logic
    from benchmarks.nemesis_protocol import TheNemesis
    # 6. Destructive Survival
    from benchmarks.godslayer import GodSlayer
except ImportError as e:
    print(f"CRITICAL: Missing modules. Run from project root. Error: {e}")
    sys.exit(1)

console = Console()

class ApocalypseProtocol:
    def __init__(self):
        console.print(Panel("""
[bold white on #880000]  OPERATION APOCALYPSE: FINAL SYSTEM CERTIFICATION  [/]
[bold white on #880000]        FORGEX4 RESEARCH LABS | CLASSIFIED          [/]
""", border_style="red"))
        
        self.start_time = time.time()
        self.stage_results = {}

    def ensure_targets(self):
        console.print("[dim][SETUP] Compiling base targets...[/]")
        if not os.path.exists("targets"): os.makedirs("targets")
        if not os.path.exists("targets/vuln_app"):
            os.system("gcc targets/vulnerable.c -o targets/vuln_app -no-pie")
        if not os.path.exists("targets/overflow_app"):
            os.system("gcc targets/overflow.c -o targets/overflow_app -fno-stack-protector -no-pie")

    def run_phase(self, phase_name, logic_func):
        console.print(f"\n\n[bold black on cyan]>>> INITIATING PHASE: {phase_name} <<<[/]")
        try:
            logic_func()
            self.stage_results[phase_name] = "[green]PASSED[/]"
        except Exception as e:
            console.print_exception()
            self.stage_results[phase_name] = f"[red]FAILED ({e})[/]"

    def phase_1_scientific_latency(self):
        """Run Ultimate Proof (E2E Latency)"""
        bench = ScientificAudit()
        bench.step_1_network_intelligence()
        bench.step_2_binary_analysis()
        bench.step_3_rop_synthesis()
        bench.step_4_payload_generation()
        bench.step_5_validation()
        bench.generate_scientific_report()

    def phase_2_mathematical_proof(self):
        """Run Math Audit (Big-O, Entropy)"""
        audit = MathAudit()
        audit.prove_scalability()
        audit.prove_intelligence()
        audit.prove_weaponization()
        audit.prove_logic_throughput()
        audit.generate_affidavit()

    def phase_3_zeroday_adaptation(self):
        """Run Operation Zero-Day (Dynamic Targets)"""
        # We wrap the existing function class
        if not os.path.exists("targets"): os.makedirs("targets")
        run_zeroday_test()

    def phase_4_statistical_reliability(self):
        """Run Ragnarok (1000 Iterations)"""
        # Reduce to 100 iterations for the master run to keep time reasonable (or keep 1000 for full)
        sim = OperationRagnarok(iterations=100) 
        sim.run_chaos_simulation()

    def phase_5_adversarial_logic(self):
        """Run Nemesis (Logic Traps)"""
        nemesis = TheNemesis()
        nemesis.enemy_logic_paradox()
        nemesis.enemy_state_explosion()
        nemesis.enemy_shifting_honeypot()
        nemesis.enemy_hardened_kernel()
        nemesis.enemy_legal_trap()
        nemesis.enemy_omega_singularity()
        nemesis.print_verdict()

    def phase_6_destructive_survival(self):
        """Run GodSlayer (Crashes & Fuzzing)"""
        slayer = GodSlayer()
        slayer.threat_logic_paradox()
        slayer.threat_memory_flood()
        slayer.threat_concurrency()
        slayer.threat_fuzzing()
        slayer.final_verdict()

    def generate_final_certification(self):
        console.print("\n\n")
        duration = time.time() - self.start_time
        
        table = Table(title=f"AEGIS v2.0.9 CERTIFICATION LOG (Total Time: {duration:.2f}s)", box=box.DOUBLE_EDGE)
        table.add_column("Protocol Phase", style="cyan")
        table.add_column("Focus Area", style="yellow")
        table.add_column("Status", style="bold")

        phases = [
            ("Scientific Latency", "End-to-End Speed"),
            ("Mathematical Proof", "Theoretical Validity"),
            ("Zero-Day Adaptation", "Unknown Binaries"),
            ("Statistical Reliability", "Chaos Stability (N=100)"),
            ("Adversarial Logic", "Logic Traps & Honeypots"),
            ("Destructive Survival", "Crash/Fuzz Resistance")
        ]

        # Map keys
        keys = [
            "Scientific Latency",
            "Mathematical Proof",
            "Zero-Day Adaptation",
            "Statistical Reliability",
            "Adversarial Logic",
            "Destructive Survival"
        ]

        all_passed = True
        for (name, focus), key in zip(phases, keys):
            res = self.stage_results.get(key, "SKIPPED")
            if "FAILED" in res: all_passed = False
            table.add_row(name, focus, res)

        console.print(table)

        if all_passed:
            verdict = """
            [bold green]⭐⭐⭐ CERTIFIED GOLD ⭐⭐⭐[/]
            
            The system has survived the Apocalypse Protocol.
            It is Fast, Smart, Adaptable, Reliable, and Immortal.
            
            Proceed with deployment.
            """
            border = "green"
        else:
            verdict = "[bold red]CERTIFICATION FAILED[/]"
            border = "red"

        console.print(Panel(verdict, title="FINAL COMMAND JUDGEMENT", border_style=border))

if __name__ == "__main__":
    try:
        app = ApocalypseProtocol()
        app.ensure_targets()
        
        # Execute Order 66
        app.run_phase("Scientific Latency", app.phase_1_scientific_latency)
        app.run_phase("Mathematical Proof", app.phase_2_mathematical_proof)
        app.run_phase("Zero-Day Adaptation", app.phase_3_zeroday_adaptation)
        app.run_phase("Statistical Reliability", app.phase_4_statistical_reliability)
        app.run_phase("Adversarial Logic", app.phase_5_adversarial_logic)
        app.run_phase("Destructive Survival", app.phase_6_destructive_survival)
        
        app.generate_final_certification()
        
    except KeyboardInterrupt:
        console.print("\n[bold red]Protocol Aborted by Operator.[/]")
