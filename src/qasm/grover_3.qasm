// Grover's Search Algorithm (3 qubits)
// Searches for |111> state
OPENQASM 3.0;
include "stdgates.inc";

qubit[3] q;
bit[3] c;

// Initialize uniform superposition
h q[0];
h q[1];
h q[2];

// Oracle: mark |111> with phase flip
h q[2];
ccx q[0], q[1], q[2];
h q[2];

// Diffusion operator
h q[0];
h q[1];
h q[2];
x q[0];
x q[1];
x q[2];
h q[2];
ccx q[0], q[1], q[2];
h q[2];
x q[0];
x q[1];
x q[2];
h q[0];
h q[1];
h q[2];

// Measure
c[0] = measure q[0];
c[1] = measure q[1];
c[2] = measure q[2];
