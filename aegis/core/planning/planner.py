from typing import List, Dict
from aegis.core.logic.engine import ReasoningEngine
from aegis.core.logic.grammar import FactType
from aegis.core.network.graph import NetworkGraph

class MissionPlan:
    """A generated checklist of actions for the autonomous agent."""
    def __init__(self, target_ip: str, steps: List[str]):
        self.target_ip = target_ip
        self.steps = steps
        self.approved = False

class AttackPlanner:
    def __init__(self, brain: ReasoningEngine, map: NetworkGraph):
        self.brain = brain
        self.map = map

    def generate_plan(self, attacker_ip: str, target_ip: str) -> MissionPlan:
        """
        1. Find physical path (NetworkX).
        2. Verify logical feasibility (Z3).
        3. Return the Mission Plan.
        """
        print(f"[PLANNER] Calculating path from {attacker_ip} -> {target_ip}")
        
        # 1. Ask the Map for the route
        # (In a real scenario, we check if route exists)
        try:
            route = nx.shortest_path(self.map.graph, attacker_ip, target_ip)
        except:
            print("[PLANNER] Error: Physical route blocked (Firewall/Airgap).")
            return MissionPlan(target_ip, [])

        # 2. Build the Action Sequence
        # For this sprint, we assume a standard Kill Chain for each hop
        actions = []
        for i in range(len(route) - 1):
            current_node = route[i]
            next_node = route[i+1]
            
            # Logic: To move from A to B, we need to Scan -> Detect -> Exploit
            actions.append(f"SCAN({next_node})")
            
            # Ask the Brain: Is exploitation mathematically possible here?
            # We assume we just found an open port
            if self.brain.analyze_feasibility(FactType.CREDENTIAL_FOUND, [FactType.PORT_OPEN]):
                actions.append(f"EXPLOIT({next_node}) -- [Verified by Z3]")
                actions.append(f"PIVOT({next_node} -> {route[i+2] if i+2 < len(route) else 'OBJECTIVE'})")
            else:
                actions.append(f"ABORT: Z3 says target {next_node} is invincible.")
                break
                
        return MissionPlan(target_ip, actions)

# Helper for the graph import (since we didn't import nx at top)
import networkx as nx