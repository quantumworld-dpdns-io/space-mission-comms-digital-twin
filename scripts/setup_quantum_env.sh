#!/usr/bin/env bash
set -euo pipefail

echo "=== Setting up Space Comms Digital Twin environment ==="

# Python
echo "--- Installing Python package ---"
pip install -e ".[dev,quantum]" 2>&1 | tail -5
echo "Python OK"

# Go
if command -v go &> /dev/null; then
    echo "Go found: $(go version)"
    cd src/go && go build ./... && cd ../..
    echo "Go OK"
else
    echo "WARNING: Go not found"
fi

# Rust
if command -v cargo &> /dev/null; then
    echo "Rust found: $(cargo --version)"
    cd src/rust && cargo build 2>&1 | tail -3 && cd ../..
    echo "Rust OK"
else
    echo "WARNING: Rust/Cargo not found"
fi

# Julia
if command -v julia &> /dev/null; then
    echo "Julia found: $(julia --version)"
    cd src/julia/SpaceCommsTwin && julia --project -e 'using Pkg; Pkg.instantiate()' 2>&1 | tail -3 && cd ../../..
    echo "Julia OK"
else
    echo "WARNING: Julia not found"
fi

# Qwik Frontend
if command -v node &> /dev/null; then
    echo "Node found: $(node --version)"
    cd src/frontend && npm install 2>&1 | tail -3 && cd ../..
    echo "Qwik/Node OK"
else
    echo "WARNING: Node.js not found"
fi

# Pre-commit
pre-commit install 2>&1 | tail -1
echo "Pre-commit hooks installed"

echo ""
echo "=== Environment setup complete ==="
