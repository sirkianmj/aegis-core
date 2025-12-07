# SPRINT 25: Field Deployment Container
# Base Image: Lightweight Python 3.11 on Linux
FROM python:3.11-slim

# metadata
LABEL maintainer="ForgeX4 Research Laboratory"
LABEL version="2.0.9"
LABEL description="AEGIS Autonomous Exploit Generation System"

# 1. Install System Dependencies (GCC for compilation, libffi for Angr)
# We clean up apt lists to keep the image small (Masterpiece optimization)
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# 2. Create Secure Workspace
WORKDIR /app

# 3. Install Python Dependencies
# We leverage caching by copying requirements first
COPY environment.yml .
# Convert conda yaml to pip (simplified for docker) or just install core libs
RUN pip install --no-cache-dir \
    z3-solver==4.12.2 \
    pydantic==2.5.2 \
    networkx==3.2.1 \
    pwntools==4.11.0 \
    angr==9.2.78 \
    capstone==5.0.0.post1 \
    fastapi uvicorn python-multipart cryptography rich

# 4. Copy the Application Code
COPY . .

# 5. Compile Targets (Pre-build the lab environment)
RUN mkdir -p targets && \
    gcc targets/vulnerable.c -o targets/vuln_app -no-pie && \
    gcc targets/overflow.c -o targets/overflow_app -fno-stack-protector -no-pie

# 6. Set Environment Variables
ENV PYTHONPATH=/app
ENV AEGIS_MODE=PRODUCTION

# 7. Expose the API Port
EXPOSE 8000

# 8. Entrypoint (Launch the API Server)
CMD ["uvicorn", "aegis.core.api.server:app", "--host", "0.0.0.0", "--port", "8000"]
