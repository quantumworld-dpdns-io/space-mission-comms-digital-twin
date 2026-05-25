use num_complex::Complex64;
use pyo3::prelude::*;

const I: Complex64 = Complex64::new(0.0, 1.0);
const ZERO: Complex64 = Complex64::new(0.0, 0.0);
const ONE: Complex64 = Complex64::new(1.0, 0.0);

fn hadamard_matrix() -> Vec<Vec<Complex64>> {
    let h = ONE / Complex64::new(2.0_f64.sqrt(), 0.0);
    vec![
        vec![h, h],
        vec![h, -h],
    ]
}

fn pauli_x_matrix() -> Vec<Vec<Complex64>> {
    vec![
        vec![ZERO, ONE],
        vec![ONE, ZERO],
    ]
}

fn pauli_y_matrix() -> Vec<Vec<Complex64>> {
    vec![
        vec![ZERO, -I],
        vec![I, ZERO],
    ]
}

fn pauli_z_matrix() -> Vec<Vec<Complex64>> {
    vec![
        vec![ONE, ZERO],
        vec![ZERO, -ONE],
    ]
}

fn cnot_matrix() -> Vec<Vec<Complex64>> {
    vec![
        vec![ONE, ZERO, ZERO, ZERO],
        vec![ZERO, ONE, ZERO, ZERO],
        vec![ZERO, ZERO, ZERO, ONE],
        vec![ZERO, ZERO, ONE, ZERO],
    ]
}

#[pyfunction]
pub fn apply_hadamard(state: &mut super::state_vector::StateVector, qubit: usize) {
    state.apply_gate(hadamard_matrix(), qubit);
}

#[pyfunction]
pub fn apply_pauli_x(state: &mut super::state_vector::StateVector, qubit: usize) {
    state.apply_gate(pauli_x_matrix(), qubit);
}

#[pyfunction]
pub fn apply_pauli_y(state: &mut super::state_vector::StateVector, qubit: usize) {
    state.apply_gate(pauli_y_matrix(), qubit);
}

#[pyfunction]
pub fn apply_pauli_z(state: &mut super::state_vector::StateVector, qubit: usize) {
    state.apply_gate(pauli_z_matrix(), qubit);
}

#[pyfunction]
pub fn apply_cnot(state: &mut super::state_vector::StateVector, control: usize, target: usize) {
    state.apply_two_qubit_gate(cnot_matrix(), control, target);
}
