# Space Comms Digital Twin — AI Agent Guide

## Project Overview

Space mission comms digital twin simulation SaaS built with Python, Go, Rust,
Julia, OpenQASM, and Qwik. Models latency, antenna visibility, and bandwidth
bottlenecks using both classical and quantum computing methods.

## Directory Structure

```
src/
  python/space_comms_digital_twin/   # Main Python package
    config/                          # Settings & constants
    classical/                       # Classical simulation (orbital, link budget)
    quantum/                         # Quantum simulation (7 frameworks)
    api/rest/                        # FastAPI REST endpoints
    services/                        # Business logic layer
    cli/                             # Click-based CLI
    visualization/                   # Plotting & dashboards
  go/                                # Go gRPC server & CLI
  rust/                              # Rust PyO3 quantum kernel
  julia/SpaceCommsTwin/              # Julia quantum optimization
  qasm/                              # OpenQASM circuit library
  frontend/                          # Qwik interactive demo
tests/
  unit/                              # pytest unit tests
  integration/                       # Integration tests
  robot/                             # Robot Framework (API + OWASP)
  benchmarks/                        # Performance benchmarks
```

## Language-Specific Commands

### Python
```bash
# Install
pip install -e ".[dev,quantum]"
# Lint & type
ruff check src/python/ tests/
mypy src/python/
# Test
pytest tests/ -v
```

### Go
```bash
cd src/go && go build ./... && go test ./...
```

### Rust
```bash
cd src/rust && cargo build && cargo test
```

### Julia
```bash
cd src/julia/SpaceCommsTwin && julia --project -e 'using Pkg; Pkg.test()'
```

### Frontend
```bash
cd src/frontend && npm install && npm run build
```

## CI/CD

- On push to `main`: full matrix build (Python, Go, Rust, Julia, Qwik)
- Robot Framework + OWASP ZAP baseline scans on every PR
- `semantic-release` creates GitHub Releases on every `main` commit
- Nightly runs: quantum integration tests + benchmarks

## Versioning

Follows Semantic Versioning (SemVer) via conventional commits:
- `feat:` → minor bump
- `fix:` → patch bump
- `BREAKING CHANGE:` → major bump

## auto_commit.sh

```bash
# Process next pending todo
./scripts/auto_commit.sh [--dry-run] [--batch N] [--lang LANG]
```
