// Decoy-State QKD Circuit
// Signal state: |+>, Decoy state: |0>
OPENQASM 3.0;
include "stdgates.inc";

qubit[4] q;
bit[4] c;

// Signal pulses (use + basis)
h q[0];
h q[1];

// Decoy pulses (use Z basis, no H)
// q[2], q[3] remain in |0>

// Channel simulation (loss and noise)
// ...

// Bob's measurement in random bases
h q[0];
h q[2];

c[0] = measure q[0];
c[1] = measure q[1];
c[2] = measure q[2];
c[3] = measure q[3];
