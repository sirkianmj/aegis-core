from pwn import *
from typing import List, Dict

class StaticAnalyzer:
    """
    Sprint 7 Component: Dangerous Sink Identification.
    Scans the Import Address Table (IAT) for known vulnerable functions.
    Replaces Ghidra Headless with Pwntools ELF Analysis (Python Native).
    """
    
    # The "Catalog of Doom" (PDF Page 12)
    DANGEROUS_SINKS = [
        "strcpy", "sprintf", "gets", "system", "execve", 
        "read", "memcpy", "strcat"
    ]

    def __init__(self, binary_path: str):
        self.binary_path = binary_path
        self.elf = ELF(binary_path, checksec=False)

    def identify_sinks(self) -> List[Dict]:
        """
        Scans the binary's symbol table for dangerous functions.
        """
        print(f"[STATIC] Scanning {self.binary_path} for dangerous sinks...")
        found_sinks = []
        
        # Iterate through all symbols in the binary
        for symbol_name, address in self.elf.symbols.items():
            # Check if this symbol is in our dangerous list
            # We strip versions (e.g., strcpy@GLIBC_2.2.5 -> strcpy)
            clean_name = symbol_name.split('@')[0]
            
            if clean_name in self.DANGEROUS_SINKS:
                print(f"[STATIC] ⚠️  FOUND SINK: {clean_name} at {hex(address)}")
                found_sinks.append({
                    "name": clean_name,
                    "address": hex(address),
                    "type": "VULNERABLE_FUNCTION"
                })
                
        if not found_sinks:
            print("[STATIC] No obvious dangerous sinks found in Import Table.")
            
        return found_sinks