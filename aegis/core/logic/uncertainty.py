from enum import Enum, auto
from typing import Optional, Callable

class TruthState(Enum):
    FALSE = 0
    TRUE = 1
    UNCERTAIN = 2

class UncertainBool:
    """
    Represents a Fact that might not be verified yet.
    Used for JIT (Just-In-Time) decision making.
    """
    def __init__(self, state: TruthState = TruthState.UNCERTAIN, confidence: float = 0.5):
        self.state = state
        self.confidence = confidence
        self._probe_callback: Optional[Callable[[], bool]] = None

    def set_probe(self, callback: Callable[[], bool]):
        """Attach a sensor (code) that can verify this fact if needed."""
        self._probe_callback = callback

    def collapse(self) -> bool:
        """
        The Observation Step.
        If the value is UNCERTAIN, trigger the probe to find the real truth.
        """
        if self.state != TruthState.UNCERTAIN:
            return self.state == TruthState.TRUE
            
        print("[JIT] Fact is UNCERTAIN. Collapsing wave function (Sending Probe)...")
        
        if self._probe_callback:
            # Execute the attached sensor (e.g., send a packet)
            result = self._probe_callback()
            self.state = TruthState.TRUE if result else TruthState.FALSE
            self.confidence = 1.0
            print(f"[JIT] Probe returned: {self.state.name}")
            return result
        else:
            print("[JIT] Error: No probe attached. Assuming False.")
            self.state = TruthState.FALSE
            return False

    def __bool__(self):
        """Allows using the object in 'if' statements directly."""
        return self.collapse()