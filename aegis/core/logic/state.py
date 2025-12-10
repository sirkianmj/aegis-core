from typing import Set, List
from .grammar import Fact, FactType

class WorldState:
    """
    HARDENING: State Persistence Logic.
    Tracks the 'Knowledge Base' as it mutates over time.
    """
    def __init__(self):
        self.known_facts: Set[str] = set()
        self.failed_actions: Set[str] = set()

    def _key(self, fact: Fact) -> str:
        return f"{fact.type.value}:{fact.target}:{fact.details}"

    def update(self, fact: Fact):
        """Add a new fact to the persistent state."""
        self.known_facts.add(self._key(fact))

    def has_fact(self, fact_type: FactType, target: str) -> bool:
        """Check if a specific type of fact exists for a target."""
        prefix = f"{fact_type.value}:{target}"
        return any(k.startswith(prefix) for k in self.known_facts)

    def mark_failure(self, action_id: str, target: str):
        """
        HARDENING: Record failure so we don't loop infinitely.
        If Scan(A) failed once, don't try it again immediately.
        """
        self.failed_actions.add(f"{action_id}:{target}")

    def is_failed(self, action_id: str, target: str) -> bool:
        return f"{action_id}:{target}" in self.failed_actions