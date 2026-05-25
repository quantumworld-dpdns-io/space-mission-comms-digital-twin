// 3-Qubit Repetition Code
// Encodes 1 logical qubit into 3 physical qubits
// Corrects single bit-flip errors
OPENQASM 3.0;
include "stdgates.inc";

qubit[4] q;  // q[0..2]: data, q[3]: ancilla
bit[2] c;    // syndrome bits

// Encode logical |0> with repetition
// |0> -> |000>
// (no gates needed for |0> encoding)

// Bit-flip error channel simulated (insert X gate on desired qubit)
// x q[0];  // uncomment to simulate error

// Syndrome measurement: parity checks
// Check qubit 0-1 parity
cx q[0], q[3];
cx q[1], q[3];
c[0] = measure q[3];

// Reset ancilla
reset q[3];

// Check qubit 1-2 parity
cx q[1], q[3];
cx q[2], q[3];
c[1] = measure q[3];

// Corrective action based on syndrome
// (classically controlled)
if (c[0] == 1 && c[1] == 1) x q[1];   // error on q[1]
if (c[0] == 1 && c[1] == 0) x q[0];   // error on q[0]
if (c[0] == 0 && c[1] == 1) x q[2];   // error on q[2]
