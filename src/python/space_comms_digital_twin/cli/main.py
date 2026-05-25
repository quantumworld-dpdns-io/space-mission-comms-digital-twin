from __future__ import annotations

import click


@click.group()
@click.version_option()
def cli():
    """Space Mission Communications Digital Twin CLI"""


@cli.group()
def simulate():
    """Run simulations"""


@simulate.command("classical")
@click.option("--distance", default=1000000.0, help="Distance in meters")
@click.option("--frequency", default=8.0, help="Frequency in GHz")
@click.option("--tx-power", default=10.0, help="Transmit power in Watts")
def simulate_classical(distance: float, frequency: float, tx_power: float):
    """Run a classical link budget simulation"""
    from space_comms_digital_twin.classical.models.link_budget import (
        LinkBudgetCalculator,
        LinkBudgetParams,
    )
    calc = LinkBudgetCalculator()
    params = LinkBudgetParams(
        distance_m=distance,
        frequency_ghz=frequency,
        tx_power_watts=tx_power,
    )
    result = calc.compute(params)
    click.echo(f"SNR: {result.snr_db:.2f} dB")
    click.echo(f"Link Margin: {result.link_margin_db:.2f} dB")
    click.echo(f"EIRP: {result.eirp_dbw:.2f} dBW")


@simulate.command("quantum")
@click.option("--backend", default="qiskit", help="Quantum backend")
@click.option("--qubits", default=2, help="Number of qubits")
@click.option("--shots", default=1024, help="Number of shots")
def simulate_quantum(backend: str, qubits: int, shots: int):
    """Run a quantum circuit simulation"""
    from space_comms_digital_twin.quantum.simulation.hybrid_simulator import HybridSimulator
    sim = HybridSimulator()
    b = sim.get_backend(backend)
    if b is None:
        click.echo(f"Backend {backend} not available")
        return
    circuit = {
        "qubits": qubits,
        "operations": [
            {"gate": "H", "qubits": [0]},
            {"gate": "CNOT", "qubits": [0, 1]},
            {"gate": "MEASURE", "qubits": [0], "classical": [0]},
            {"gate": "MEASURE", "qubits": [1], "classical": [1]},
        ],
    }
    result = b.run_circuit(circuit, shots=shots)
    click.echo(f"Counts: {result.counts}")
    click.echo(f"Backend: {result.backend_name}")


@cli.group()
def quantum():
    """Quantum operations"""


@quantum.command("qkd")
@click.option("--protocol", default="BB84", help="QKD protocol")
@click.option("--bits", default=256, help="Number of bits")
def run_qkd(protocol: str, bits: int):
    """Run quantum key distribution"""
    from space_comms_digital_twin.quantum.comms.qkd_protocol import BB84
    qkd = BB84(num_bits=bits)
    result = qkd.run()
    click.echo(f"QBER: {result.qber:.4f}")
    click.echo(f"Key rate: {result.key_rate:.4f}")
    click.echo(f"Key length: {result.key_length}")


@quantum.command("teleport")
def run_teleport():
    """Run quantum teleportation"""
    from space_comms_digital_twin.quantum.comms.teleportation import QuantumTeleportation
    tp = QuantumTeleportation()
    result = tp.run()
    click.echo(f"Success: {result.success}")
    click.echo(f"Fidelity: {result.fidelity:.4f}")


@cli.group()
def optimize():
    """Run optimizations"""


@optimize.command("qaoa")
@click.option("--qubits", default=4, help="Number of qubits")
@click.option("--layers", default=1, help="QAOA layers")
def run_qaoa(qubits: int, layers: int):
    """Run QAOA optimization"""
    from space_comms_digital_twin.quantum.optimization.qaoa import QAOA
    qaoa = QAOA(n_layers=layers)
    edges = [(0, 1), (0, 2), (1, 2)]
    H = qaoa.build_maxcut_hamiltonian(edges, qubits)
    result = qaoa.solve(H)
    click.echo(f"Optimal value: {result.optimal_value:.4f}")
    click.echo(f"Approximation ratio: {result.approximation_ratio:.4f}")


@optimize.command("vqe")
@click.option("--qubits", default=2, help="Number of qubits")
def run_vqe(qubits: int):
    """Run VQE optimization"""
    from space_comms_digital_twin.quantum.optimization.vqe import VQE
    vqe = VQE(n_qubits=qubits)
    pauli = [("ZZ", -1.0), ("II", -0.5)]
    H = vqe.build_hamiltonian(pauli)
    result = vqe.solve(H)
    click.echo(f"Optimal energy: {result.optimal_energy:.4f}")


@cli.group()
def serve():
    """Start API server"""


@serve.command("start")
@click.option("--host", default="0.0.0.0", help="Host to bind")
@click.option("--port", default=8000, help="Port to bind")
@click.option("--reload", is_flag=True, help="Enable auto-reload")
def start_server(host: str, port: int, reload: bool):
    """Start the FastAPI server"""
    import uvicorn
    uvicorn.run("space_comms_digital_twin.api.rest.app:app", host=host, port=port, reload=reload)


@cli.command("backends")
def list_backends():
    """List available quantum backends"""
    from rich.console import Console
    from rich.table import Table
    from space_comms_digital_twin.quantum.simulation.hybrid_simulator import HybridSimulator

    sim = HybridSimulator()
    backends = sim.list_backends()

    console = Console()
    table = Table(title="Available Quantum Backends")
    table.add_column("Name", style="cyan")
    table.add_column("Max Qubits", style="green")
    table.add_column("Gate Set")

    for b in backends:
        table.add_row(b["name"], str(b["max_qubits"]), ", ".join(b["gate_set"][:8]) + "...")

    console.print(table)
