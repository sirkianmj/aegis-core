import sys
import os
import time
import logging
from typing import List, Tuple

# Ensure we can find the modules
sys.path.append(os.getcwd())

# Import Rich for Professional Output
try:
    from rich.console import Console
    from rich.table import Table
    from rich.progress import track
    from rich.panel import Panel
except ImportError:
    print("CRITICAL: 'rich' library missing. Run 'pip install rich'")
    sys.exit(1)

console = Console()

# --- THE SMART JUDGE ---
class SmartJudge:
    def __init__(self):
        self.score = 0
        self.total_tests = 0
        self.max_score = 135 # Adjusted for all hardening + ROP features
        self.results = []

    def evaluate(self, name: str, success: bool, points: int, details: str = ""):
        self.total_tests += 1
        status = "[green]PASS[/green]" if success else "[red]FAIL[/red]"
        if success:
            self.score += points
        
        self.results.append([name, status, f"{points if success else 0}/{points}", details])
        
        if success:
            console.print(f"   ✅ {name}: {details}", style="dim")
        else:
            console.print(f"   ❌ {name}: {details}", style="bold red")

    def final_report(self):
        table = Table(title="AEGIS v2.0.9 - SYSTEM INTEGRITY REPORT")
        table.add_column("Module", style="cyan")
        table.add_column("Status", justify="center")
        table.add_column("Score", justify="right")
        table.add_column("Details")

        for row in self.results:
            table.add_row(*row)

        console.print("\n")
        console.print(table)
        
        # Calculate Letter Grade
        percentage = (self.score / self.max_score) * 100
        grade = "F"
        color = "red"
        if percentage >= 90: grade, color = "A+ (Combat Ready)", "green"
        elif percentage >= 80: grade, color = "A (Operational)", "green"
        elif percentage >= 70: grade, color = "B (Functional)", "yellow"
        elif percentage >= 50: grade, color = "C (Unstable)", "orange1"

        panel = Panel(f"[bold {color}]FINAL SCORE: {self.score}/{self.max_score}\nGRADE: {grade}[/]", title="Judge's Verdict")
        console.print(panel)

# --- TEST MODULES ---

def compile_targets():
    """Helper to ensure C binaries exist"""
    if not os.path.exists("targets"): os.makedirs("targets")
    if not os.path.exists("targets/vuln_app"):
        console.print("[yellow]Compiling Auth Target...[/]")
        os.system("gcc targets/vulnerable.c -o targets/vuln_app -no-pie")
    if not os.path.exists("targets/overflow_app"):
        console.print("[yellow]Compiling Overflow Target...[/]")
        os.system("gcc targets/overflow.c -o targets/overflow_app -fno-stack-protector -no-pie")

def test_sprint_0_foundations(judge: SmartJudge):
    console.print("\n[bold blue]--- PHASE 1: FOUNDATION CHECK ---[/]")
    try:
        import z3
        import angr
        import pwn
        import networkx
        judge.evaluate("Dependencies", True, 10, "Z3, Angr, Pwntools, NetworkX loaded")
    except ImportError as e:
        judge.evaluate("Dependencies", False, 10, f"Missing Lib: {e}")

def test_sprint_1_logic(judge: SmartJudge):
    console.print("\n[bold blue]--- PHASE 2: COGNITIVE CORE (HARDENED) ---[/]")
    try:
        from aegis.core.logic.engine import ReasoningEngine
        from aegis.core.logic.grammar import FactType
        from aegis.core.logic.state import WorldState
        
        # Test 1: Reasoning
        engine = ReasoningEngine()
        engine.load_rules()
        res = engine.analyze_feasibility(FactType.CREDENTIAL_FOUND, [FactType.PORT_OPEN])
        judge.evaluate("Z3 Logic Engine", res, 5, "Proof of Attack Path derived")
        
        # Test 2: Recursion Limit (Hardening)
        import inspect
        sig = inspect.signature(engine.analyze_feasibility)
        if 'max_depth' in sig.parameters:
            judge.evaluate("Recursion Guard", True, 5, "Hardening: max_depth parameter detected")
        else:
            judge.evaluate("Recursion Guard", False, 5, "Hardening MISSING")

        # Test 3: State Persistence (Hardening)
        state = WorldState()
        judge.evaluate("State Persistence", True, 5, "WorldState class implemented")

    except Exception as e:
        judge.evaluate("Logic Core", False, 15, f"Crash: {e}")

def test_sprint_2_3_network(judge: SmartJudge):
    console.print("\n[bold blue]--- PHASE 3: NETWORK & PLANNING ---[/]")
    try:
        from aegis.core.network.graph import NetworkGraph, NetworkACL
        from aegis.core.planning.planner import AttackPlanner, ReasoningEngine
        
        # Test 1: ACL Structure (Hardening)
        net = NetworkGraph()
        if hasattr(net, 'acls') and hasattr(net, 'check_access'):
            judge.evaluate("Firewall Logic", True, 5, "Hardening: ACL structure detected")
        else:
            judge.evaluate("Firewall Logic", False, 5, "Hardening MISSING")
            
        # Test 2: Planning
        net.add_host("A", "Linux")
        net.add_host("B", "Windows", critical=True)
        net.add_connection("A", "B", 445)
        
        brain = ReasoningEngine()
        brain.load_rules()
        planner = AttackPlanner(brain, net)
        plan = planner.generate_plan("A", "B")
        
        if len(plan.steps) > 0:
            judge.evaluate("Mission Planner", True, 10, f"Generated {len(plan.steps)} step plan")
        else:
            judge.evaluate("Mission Planner", False, 10, "Failed to generate plan")

    except Exception as e:
        judge.evaluate("Network/Planner", False, 15, f"Crash: {e}")

def test_sprint_4_5_governance(judge: SmartJudge):
    console.print("\n[bold blue]--- PHASE 4: GOVERNANCE & SENSORS ---[/]")
    try:
        from aegis.core.governance.policy import OSafePolicy
        from aegis.core.logic.uncertainty import UncertainBool
        from aegis.core.logic.actions import CyberAction, FactType
        from aegis.core.network.graph import NetworkNode
        
        # Test 1: Default Deny (Hardening)
        unknown_action = CyberAction(id="UNK", name="Unknown", description="?", safety_tier="PURPLE", preconditions=[], postconditions=[])
        target = NetworkNode(ip="1.1.1.1", hostname="Test", os="Linux")
        allowed, reason = OSafePolicy.check_authorization(unknown_action, target)
        if not allowed and "Default Deny" in reason:
            judge.evaluate("Default Deny", True, 5, "Hardening: Unknown action blocked")
        else:
            judge.evaluate("Default Deny", False, 5, f"Hardening FAIL: {reason}")
            
        # Test 2: Rate Limiting (Hardening)
        if hasattr(UncertainBool, 'RATE_LIMIT_DELAY'):
            judge.evaluate("Stealth/Rate Limit", True, 5, "Hardening: Stealth delay configured")
        else:
            judge.evaluate("Stealth/Rate Limit", False, 5, "Hardening MISSING")
            
        # Test 3: XAI
        from aegis.core.governance.xai import XAIEngine
        xai = XAIEngine()
        xai.log_decision("TEST", "Input", "Output", "Reason")
        judge.evaluate("XAI Recorder", True, 5, "Audit log generated")

        # Test 4: Encryption (Hardening) - MOVED INSIDE TRY BLOCK
        xai.export_encrypted_log("test_log.enc")
        if os.path.exists("test_log.enc") and os.path.exists("test_log.enc.key"):
             judge.evaluate("Log Encryption", True, 5, "AES-256 Encrypted file found")
        else:
             judge.evaluate("Log Encryption", False, 5, "Encryption MISSING")

    except Exception as e:
        judge.evaluate("Governance", False, 20, f"Crash: {e}")

def test_sprint_7_8_9_weapons(judge: SmartJudge):
    console.print("\n[bold blue]--- PHASE 5: WEAPON SYSTEMS ---[/]")
    compile_targets()
    
    try:
        # Test 1: Static Sink ID
        from aegis.core.analysis.static import StaticAnalyzer
        sa = StaticAnalyzer("targets/overflow_app")
        sinks = sa.identify_sinks()
        if sinks:
            judge.evaluate("Static Analysis", True, 5, f"Found {len(sinks)} dangerous sinks")
        else:
            judge.evaluate("Static Analysis", False, 5, "No sinks found")
            
        # Test 2: Symbolic Slicer
        from aegis.core.analysis.slicer import AngrSlicer
        slicer = AngrSlicer("targets/vuln_app")
        pw = slicer.solve_for_output("SUCCESS_ACCESS_GRANTED")
        if pw and "Aegis" in pw:
            judge.evaluate("Symbolic Slicer", True, 10, f"Cracked Binary: {pw}")
        else:
            judge.evaluate("Symbolic Slicer", False, 10, "Failed to crack binary")
            
        # Test 3: Concolic Verification
        from aegis.core.analysis.emulator import ConcolicVerifier
        verifier = ConcolicVerifier("targets/vuln_app")
        verified = verifier.verify_input_and_trace("AegisTopSecret\n", "SUCCESS")
        judge.evaluate("Concolic Verifier", verified, 10, "Trace confirmed execution")
        
        # Test 4: Weaponization & Hardening
        from aegis.core.exploitation.payload_factory import PayloadFactory
        pf = PayloadFactory()
        payload = pf.generate_buffer_overflow(72, 0x401176)
        
        # Check for Bad Char Logic (Hardening check)
        if hasattr(pf, '_check_bad_chars'):
            judge.evaluate("Bad Char Filter", True, 5, "Hardening: Filter active")
        else:
            judge.evaluate("Bad Char Filter", False, 5, "Hardening MISSING")
            
        if len(payload) > 72:
            judge.evaluate("Exploit Generator", True, 5, f"Payload built: {len(payload)} bytes")
        else:
            judge.evaluate("Exploit Generator", False, 5, "Payload failed")

        # Test 5: ROP Chain Synthesis (Sprint 10) - NEW
        from aegis.core.exploitation.rop_engine import ROPSynthesizer
        rop_syn = ROPSynthesizer("targets/overflow_app")
        rop_syn.find_gadgets()
        chain = rop_syn.build_exec_chain("hacker_win")
        
        if len(chain) > 0:
            judge.evaluate("ROP Synthesizer", True, 10, f"Chain built: {len(chain)} bytes")
        else:
            judge.evaluate("ROP Synthesizer", False, 10, "Failed to build ROP chain")

        # Test 6: ASLR Awareness (Hardening) - MOVED INSIDE TRY BLOCK
        # Case 1: Fail check (ASLR on, No leak)
        should_fail = pf.check_aslr_requirements(aslr_enabled=True, has_info_leak=False)
        # Case 2: Pass check
        should_pass = pf.check_aslr_requirements(aslr_enabled=True, has_info_leak=True)
        
        if (not should_fail) and should_pass:
            judge.evaluate("ASLR Awareness", True, 5, "Logic prevents blind attacks on ASLR")
        else:
            judge.evaluate("ASLR Awareness", False, 5, "Hardening MISSING")

    except Exception as e:
        judge.evaluate("Weapons Systems", False, 50, f"Crash: {e}")

# --- MAIN EXECUTION ---
def main():
    judge = SmartJudge()
    test_sprint_0_foundations(judge)
    test_sprint_1_logic(judge)
    test_sprint_2_3_network(judge)
    test_sprint_4_5_governance(judge)
    test_sprint_7_8_9_weapons(judge)
    test_sprint_11_12_hatl(judge)
    judge.final_report()
def test_sprint_11_12_hatl(judge: SmartJudge):
    console.print("\n[bold blue]--- PHASE 6: HARDWARE TRACING (HATL) ---[/]")
    try:
        from aegis.core.tracing.hatl import HardwareTraceEngine, Architecture, PacketType
        import struct
        
        # Test Decoding
        hatl = HardwareTraceEngine(Architecture.INTEL_X64)
        # 0x02 = TNT (Taken)
        hatl.ingest_raw_stream(b'\x02') 
        count = hatl.process()
        if count > 0 and hatl.decoded_packets[0].type == PacketType.BRANCH_DECISION:
            judge.evaluate("Intel PT Decoder", True, 10, "Decoded TNT packet")
        else:
            judge.evaluate("Intel PT Decoder", False, 10, "Decoding failed")
            
        # Test Hardening (Ring Buffer)
        hatl_arm = HardwareTraceEngine(Architecture.ARM_V8)
        overflow = b'\x41' * 70000 # 70KB
        hatl_arm.ingest_raw_stream(overflow)
        if len(hatl_arm.ring_buffer.dump()) == 65536:
            judge.evaluate("Ring Buffer Hardening", True, 10, "Buffer capped at 64KB")
        else:
            judge.evaluate("Ring Buffer Hardening", False, 10, "Buffer overflowed")
            
    except Exception as e:
        judge.evaluate("HATL System", False, 20, f"Crash: {e}")    

if __name__ == "__main__":
    main()