// Quantum Teleportation Circuit
// Teleports a quantum state from qubit 0 to qubit 2
OPENQASM 3.0;
include "stdgates.inc";

qubit[3] q;
bit[2] c;

// Prepare initial state on q[0]
h q[0];

// Create Bell pair between q[1] and q[2]
h q[1];
cx q[1], q[2];

// Alice's operations
cx q[0], q[1];
h q[0];

// Alice measures
c[0] = measure q[0];
c[1] = measure q[1];

// Bob's corrections (classically controlled)
if (c[1] == 1) x q[2];
if (c[0] == 1) z q[2];
