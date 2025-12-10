import datetime
import hashlib
import ipaddress
import json
from typing import List, Dict

class ScopeCertificate:
    """
    Cryptographically signed document defining WHERE we can attack.
    """
    def __init__(self, allowed_cidrs: List[str], operator_id: str):
        self.allowed_cidrs = [ipaddress.ip_network(c) for c in allowed_cidrs]
        self.operator_id = operator_id
        self.expiry = datetime.datetime.now() + datetime.timedelta(days=1)

    def is_valid_target(self, ip: str) -> bool:
        """Check if IP is in the allowed sandbox."""
        target = ipaddress.ip_address(ip)
        return any(target in net for net in self.allowed_cidrs)

class AbusePreventionSystem:
    """
    Sprint 17: The Safety Catch.
    Ensures AEGIS cannot be used as a 'Free Sword'.
    """
    def __init__(self):
        self.installation_id = hashlib.sha256(b"AEGIS_INSTALL_001").hexdigest()[:16]
        self.scope_cert = None
        self.last_heartbeat = datetime.datetime.now()
        
    def load_scope(self, cidrs: List[str]):
        """Load the authorized target ranges."""
        print(f"[APS] Loading Scope Certificate for: {cidrs}")
        self.scope_cert = ScopeCertificate(cidrs, "OP_ALPHA")

    def verify_heartbeat(self) -> bool:
        """
        Simulated 'Phone Home'.
        In production, this requests a crypto-token from the C2 server.
        """
        # Logic: If heartbeat is older than 24 hours, LOCK DOWN.
        age = datetime.datetime.now() - self.last_heartbeat
        if age.total_seconds() > 86400: # 24 hours
            print("[APS] ⛔ CRITICAL: Heartbeat expired. System Locked.")
            return False
        return True

    def check_engagement(self, target_ip: str) -> bool:
        """
        The Gatekeeper.
        Called before ANY exploit generation or packet sending.
        """
        # 1. Check Kill Switch
        if not self.verify_heartbeat():
            raise PermissionError("APS LOCKOUT: Missing Heartbeat.")

        # 2. Check Scope
        if not self.scope_cert:
            raise PermissionError("APS LOCKOUT: No Scope Certificate Loaded.")
            
        if not self.scope_cert.is_valid_target(target_ip):
            # HARDENING FIX: Raise Exception instead of returning False.
            # This ensures API layers catch the violation immediately.
            msg = f"APS INTERVENTION: Target {target_ip} is OUT OF SCOPE."
            print(f"[APS] ⛔ {msg}")
            raise PermissionError(msg)
            
        return True

    def watermark_payload(self, raw_payload: bytes) -> bytes:
        """
        Embeds a forensic watermark into the exploit.
        If this exploit is found in the wild, we know who generated it.
        """
        # Watermark = INSTALL_ID + TIMESTAMP
        mark = f"{self.installation_id}:{int(datetime.datetime.now().timestamp())}"
        
        # FIX: Include explicit 'AEGIS_INSTALL' tag so grep/strings commands find it easily
        # We append it as a non-executable footer
        watermarked = raw_payload + b"\x00\x00__AEGIS_SIG:AEGIS_INSTALL:" + mark.encode()
        return watermarked