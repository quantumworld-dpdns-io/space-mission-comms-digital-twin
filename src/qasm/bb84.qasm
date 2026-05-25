// BB84 QKD Preparation Circuit
// Generates random bits in random bases for quantum key distribution
OPENQASM 3.0;
include "stdgates.inc";

qubit[8] q;
bit[8] c;

// Alice's random bit generation and encoding
// Basis encoding: H = + basis (0), no H = Z basis (1)
h q[0];
h q[2];
h q[4];
h q[6];

// Bit encoding: X for 1, I for 0
x q[1];
x q[3];
x q[5];

// Send to Bob (channel simulation)
// Bob's random measurement basis
h q[0];
h q[1];
h q[3];
h q[4];
h q[6];
h q[7];

// Measure
c[0] = measure q[0];
c[1] = measure q[1];
c[2] = measure q[2];
c[3] = measure q[3];
c[4] = measure q[4];
c[5] = measure q[5];
c[6] = measure q[6];
c[7] = measure q[7];
