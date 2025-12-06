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

    def analyze_feasibility(self, goal: FactType, initial_state: List[FactType]) -> bool:
        """
        Ask Z3: "Given the initial state, is there a valid mathematical path to the Goal?"
        """
        self.solver.push() # Save state
        
        # 1. Assert Initial State is TRUE
        for fact in initial_state:
            self.solver.add(self._get_var(fact) == True)
            
        # 2. We want to know if the GOAL is reachable.
        # In a full planner (Sprint 3), we solve for the sequence.
        # For Sprint 1, we just check if the logic is consistent with the goal being True.
        goal_var = self._get_var(goal)
        
        # We verify if there exists a model where Goal is True
        self.solver.add(goal_var == True)
        
        result = self.solver.check()
        self.solver.pop() # Restore state
        
        return result == z3.sat