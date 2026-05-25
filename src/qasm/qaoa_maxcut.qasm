// QAOA for MaxCut on 2-node graph
// p=1 layer with parameters gamma=0.5, beta=0.3
OPENQASM 3.0;
include "stdgates.inc";

qubit[2] q;

// Initial state: uniform superposition
h q[0];
h q[1];

// Phase separation (gamma layer)
cx q[1], q[0];
rz(0.5) q[0];
cx q[1], q[0];

// Mixing (beta layer)
rx(0.3) q[0];
rx(0.3) q[1];

// Measure
bit[2] c;
c[0] = measure q[0];
c[1] = measure q[1];
