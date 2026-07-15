# Space Mission Comms Digital Twin

[![CI](https://github.com/quantumworld-dpdns-io/space-mission-comms-digital-twin/actions/workflows/ci.yml/badge.svg)](https://github.com/quantumworld-dpdns-io/space-mission-comms-digital-twin/actions/workflows/ci.yml)
[![Release](https://github.com/quantumworld-dpdns-io/space-mission-comms-digital-twin/actions/workflows/release.yml/badge.svg)](https://github.com/quantumworld-dpdns-io/space-mission-comms-digital-twin/actions/workflows/release.yml)
[![Security Scan](https://github.com/quantumworld-dpdns-io/space-mission-comms-digital-twin/actions/workflows/security-scan.yml/badge.svg)](https://github.com/quantumworld-dpdns-io/space-mission-comms-digital-twin/actions/workflows/security-scan.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

> Space mission comms digital twin – simulation SaaS modeling latency, antenna visibility, and bandwidth bottlenecks before launch. Integrates 7 quantum computing frameworks for hybrid classical-quantum simulation.

## Architecture

```
┌──────────────────────────────────────────────┐
│           Qwik Frontend (Interactive Demo)     │
├──────────────────────────────────────────────┤
│           FastAPI REST API (Python)            │
├──────────────────────────────────────────────┤
│  Classical Sim.  │  Quantum Sim. (7 SDKs)     │
│  ─────────────── │  ─────────────────        │
│  • Orbital       │  • Qiskit                 │
│  • Link Budget   │  • Cirq                    │
│  • Visibility    │  • PennyLane               │
│  • Latency       │  • QuTiP                   │
│  • Bandwidth     │  • CUDA-Q (GPU)            │
│                  │  • Amazon Braket            │
│                  │  • Strawberry Fields        │
├──────────────────────────────────────────────┤
│  Go gRPC  │ Rust PyO3 │ Julia Opt │ OpenQASM │
├──────────────────────────────────────────────┤
│  CI/CD (GitHub Actions) │ Robot + OWASP Sec  │
└──────────────────────────────────────────────┘
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Languages** | Python 3.11+, Go 1.22, Rust 2021, Julia 1.10, OpenQASM 3.0 |
| **Frontend** | Qwik, TypeScript, Vite |
| **Quantum SDKs** | Qiskit, Cirq, PennyLane, QuTiP, Amazon Braket, Strawberry Fields, CUDA-Q |
| **Classical** | NumPy, SciPy, Astropy, SGP4 |
| **API** | FastAPI, Pydantic, Uvicorn |
| **CLI** | Click, Rich |
| **Testing** | pytest, Robot Framework, OWASP ZAP |
| **CI/CD** | GitHub Actions, semantic-release |
| **Container** | Docker, Kubernetes, Helm |

## Quick Start

```bash
# Python package
pip install -e ".[dev,quantum]"

# Setup all languages
./scripts/setup_quantum_env.sh

# Run tests
pytest tests/ -v

# Start API server
sct serve start --port 8000

# Run CLI simulation
sct simulate classical --distance 1000000 --frequency 8.0
sct simulate quantum --backend qiskit --qubits 2

# Run QKD
sct quantum qkd --protocol BB84 --bits 256
```

## CLI Usage

```
sct simulate classical   Run link budget analysis
sct simulate quantum     Run quantum circuit simulation  
sct quantum qkd          Run QKD protocol
sct quantum teleport     Run quantum teleportation
sct optimize qaoa        Run QAOA optimization
sct optimize vqe         Run VQE optimization
sct serve start          Start API server
sct backends             List quantum backends
```

## Quantum Frameworks

| Backend | Type | Max Qubits | GPU Support |
|---------|------|------------|-------------|
| Qiskit | Circuit + Aer Sim | 32 | No |
| Cirq | Circuit + qsim | 25 | No |
| PennyLane | QML + Lightning | 20 | Yes |
| QuTiP | Open Dynamics | 12 | Yes (JAX) |
| CUDA-Q | GPU Simulator | 30 | Yes (NVIDIA) |
| Amazon Braket | Multi-vendor | 25 | No |
| Strawberry Fields | Photonic CV | 6 | No |

## Project Structure

```
src/
  python/space_comms_digital_twin/   # Main Python package
    config/                          # Settings & constants
    classical/                       # Classical simulation
    quantum/                         # Quantum simulation (7 frameworks)
      comms/                         # QKD, teleportation, error correction
      simulation/                    # Backend implementations
      optimization/                  # QAOA, VQE, annealing, Grover
      ml/                            # QSVM, QNN, anomaly detection
    api/rest/                        # FastAPI REST endpoints
    services/                        # Business logic
    cli/                             # Click CLI
    visualization/                   # Plotting
  go/                                # Go gRPC server
  rust/                              # Rust PyO3 kernel
  julia/SpaceCommsTwin/              # Julia optimization
  qasm/                              # OpenQASM circuits
  frontend/                          # Qwik interactive demo
tests/
  unit/                              # pytest unit tests
  integration/                       # Integration tests
  robot/                             # Robot Framework (OWASP)
  benchmarks/                        # Performance benchmarks
```

## CI/CD

- **CI**: lint, typecheck, test, security scan on every push/PR
- **Quantum Integration**: nightly quantum benchmark suite
- **Security**: OWASP ZAP baseline + Robot Framework on every PR
- **Release**: `semantic-release` on every `main` commit → PyPI + Docker
- **Auto-commit**: `scripts/auto_commit.sh` processes TODOS.md

## OWASP Top 10 Coverage

All OWASP Top 10 (2021) categories tested via Robot Framework:
A01-A10 including injection, broken auth, SSRF, crypto failures, and more.

## License

[MIT](LICENSE) © 2026 quantumworld-dpdns-io


---
Julia language: [#JuliaLang](https://julialang.org/) | [JuliaLang GitHub](https://github.com/JuliaLang/julia)
