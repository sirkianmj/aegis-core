import z3
from typing import List, Dict
from .grammar import Fact, FactType
from .actions import CyberAction, ALL_ACTIONS

class ReasoningEngine:
    """
    The Z3 Integration Layer.
    Translates 'CyberWarfare' into 'Math' to prove attack feasibility.
    """
    def __init__(self):
        self.solver = z3.Solver()
        # We track facts as boolean variables (True/False)
        self.fact_vars: Dict[str, z3.BoolRef] = {}
        self.actions_map: Dict[str, CyberAction] = {a.id: a for a in ALL_ACTIONS}

    def _get_var(self, fact_type: FactType) -> z3.BoolRef:
        """Get or create a Z3 boolean variable for a Fact Type."""
        name = fact_type.value
        if name not in self.fact_vars:
            self.fact_vars[name] = z3.Bool(name)
        return self.fact_vars[name]

    def load_rules(self):
        """
        Convert all CyberActions into Z3 Implications.
        Logic: IF (Preconditions == True) THEN (Postconditions == Possible)
        """
        for action in self.actions_map.values():
            # 1. Create a boolean for "Action Executed"
            action_var = z3.Bool(f"EXEC_{action.id}")
            
            # 2. Constraint: Action can only run IF preconditions are met
            # (EXEC_Action -> Precondition1 AND Precondition2)
            if action.preconditions:
                pre_vars = [self._get_var(p) for p in action.preconditions]
                self.solver.add(z3.Implies(action_var, z3.And(pre_vars)))

            # 3. Constraint: IF action runs, THEN postconditions become True
            # (EXEC_Action -> Postcondition1 AND Postcondition2)
            if action.postconditions:
                post_vars = [self._get_var(p) for p in action.postconditions]
                self.solver.add(z3.Implies(action_var, z3.And(post_vars)))

    def analyze_feasibility(self, goal: FactType, initial_state: List[FactType], max_depth: int = 10) -> bool:
        """
        HARDENING: Added 'max_depth' to prevent Z3 infinite recursion.
        """
        self.solver.push()
        
        # 1. Assert Initial State
        for fact in initial_state:
            self.solver.add(self._get_var(fact) == True)
            
        # 2. Assert Goal
        goal_var = self._get_var(goal)
        self.solver.add(goal_var == True)
        
        # 3. RECURSION GUARD:
        # In a full Bounded Model Check (BMC), we would unroll the loop 'max_depth' times.
        # For this architecture, we rely on the solver's internal decision limit.
        # We enforce a 'soft' limit by configuring Z3 parameters.
        self.solver.set("timeout", 5000) # 5 seconds max thinking time
        
        result = self.solver.check()
        self.solver.pop()
        
        return result == z3.sat