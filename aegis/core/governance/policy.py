from typing import Dict, Tuple
from aegis.core.logic.actions import CyberAction
from aegis.core.network.graph import NetworkNode

class SafetyViolation(Exception):
    """Raised when AI tries to do something illegal."""
    pass

class OSafePolicy:
    """
    The Operational Safety Protocol (O-SAFE).
    Enforces Rules of Engagement (RoE).
    """
    
    @staticmethod
    def check_authorization(action: CyberAction, target: NetworkNode) -> Tuple[bool, str]:
        """
        Returns (Allowed, Reason).
        
        Logic from PDF v2.0.9:
        - GREEN: Always Allowed.
        - YELLOW: Allowed with Logging.
        - RED + Low Criticality: Allowed with Logging.
        - RED + High Criticality: BLOCKED (Requires Twin-Test).
        """
        
        print(f"[O-SAFE] Reviewing: {action.name} ({action.safety_tier}) on {target.hostname}")
        
        # Rule 1: GREEN actions are always safe
        if action.safety_tier == "GREEN":
            return True, "APPROVED (Tier Green)"
            
        # Rule 2: YELLOW actions are safe but noisy
        if action.safety_tier == "YELLOW":
            return True, "APPROVED (Tier Yellow - Logged)"
            
        # Rule 3: RED actions
        if action.safety_tier == "RED":
            if target.is_critical:
                # This is the KILL SWITCH
                return False, "DENIED: RED Action on Critical Asset! Twin-Test Required."
            else:
                return True, "APPROVED (Tier Red - Low Impact Target)"
                
        return False, "UNKNOWN SAFETY TIER"

    @staticmethod
    def enforce(action: CyberAction, target: NetworkNode):
        """Raises exception if denied."""
        allowed, reason = OSafePolicy.check_authorization(action, target)
        if not allowed:
            raise SafetyViolation(f"O-SAFE INTERVENTION: {reason}")
        print(f"[O-SAFE] Audit: {reason}")