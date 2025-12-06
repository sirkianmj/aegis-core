import z3
from typing import Dict, List, Set
from .grammar import Fact, FactType, AccessLevel

class KnowledgeBase:
    """
    The Z3 Solver Context. 
    This manages the timeline of the attack.
    """
    def __init__(self):
        self.solver = z3.Solver()
        self.facts: Dict[str, z3.BoolRef] = {}
        
    def _get_fact_key(self, fact: Fact) -> str:
        """Create a unique string key for Z3 variables."""
        return f"{fact.type.value}_{fact.target}_{fact.details}"

    def add_initial_knowledge(self, known_facts: List[Fact]):
        """Populate the world with starting truth."""
        for fact in known_facts:
            key = self._get_fact_key(fact)
            if key not in self.facts:
                # Create a Z3 Boolean variable
                self.facts[key] = z3.Bool(key)
            
            # Assert that this fact is TRUE in the initial state
            self.solver.add(self.facts[key] == True)

    def check_reachability(self, target_fact: Fact) -> bool:
        """
        Ask Z3: "Is it mathematically possible for this Fact to be True?"
        """
        key = self._get_fact_key(target_fact)
        if key not in self.facts:
            # If the variable doesn't exist, we assume it's theoretically possible 
            # but currently unknown. For now, we create it.
            self.facts[key] = z3.Bool(key)
            
        # Push a new scope so we don't mess up the permanent state
        self.solver.push()
        
        # We want to know if 'target_fact' CAN be true given constraints
        # For a scanner, we often check if pre-conditions imply post-conditions
        # But for now, let's just check consistency
        result = self.solver.check()
        
        self.solver.pop()
        return result == z3.sat