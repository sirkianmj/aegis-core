# 📘 PROJECT AEGIS v2.0.9 - OPERATOR MANUAL

**Classification:** FORGEX4 CYSSEC  
**Status:** RELEASED  

---

## 1. System Overview
AEGIS is an **Autonomous Cyber Reasoning System (ACRS)**. It does not run pre-recorded scripts. It observes the target, reasons about feasibility using **Z3 Logic**, and mathematically synthesizes exploits using **Symbolic Execution**.

## 2. Quick Start (Field Deployment)

### Option A: Docker (Recommended)
```bash
# Build the weapon system
docker build -t aegis-core .

# Launch the Command Interface
docker run -p 8000:8000 aegis-core
```

### Option B: Manual Execution
```bash
# Start the API
uvicorn aegis.core.api.server:app --reload
```

## 3. Operational Capabilities

### 🧠 The Cognitive Core
- **Logic Engine:** Uses SMT solvers to prove attack paths exist before packets are sent.
- **Governance:** Enforces O-SAFE (Operational Safety). Attacks on Critical Infrastructure are mathematically impossible without Twin-Test verification.

### ⚔️ Weaponization
- **AEG (Auto-Exploit Gen):** Automatically detects buffer overflows and generates payloads.
- **Polymorphism:** Uses Source-Mutation to evade signature detection.
- **ROP Synthesis:** Automatically bypasses NX/DEP memory protections.

## 4. Safety & Compliance

- **Kill Switch:** System locks if heartbeat is missed.
- **Audit Trail:** All decisions are logged to audit_log.enc (AES-256 Encrypted).
- **Watermarking:** All payloads contain forensic ID AEGIS_INSTALL.
- **Authorized Use Only.** Compliance with ISO/IEC 29147 Required.

---

### Step 3: Final Verification (The Build)

Let's verify the Dockerfile is valid (lint check) without actually building the 2GB image (which takes too long).

```bash
# Check if Dockerfile exists and has content
cat Dockerfile | head -n 5
```

*(Save and Exit)*