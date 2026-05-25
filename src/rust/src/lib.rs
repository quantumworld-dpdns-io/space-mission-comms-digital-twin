use pyo3::prelude::*;

mod state_vector;
mod gates;

#[pymodule]
fn space_comms_quantum_kernel(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<state_vector::StateVector>()?;
    m.add_function(wrap_pyfunction!(gates::apply_hadamard, m)?)?;
    m.add_function(wrap_pyfunction!(gates::apply_pauli_x, m)?)?;
    m.add_function(wrap_pyfunction!(gates::apply_pauli_y, m)?)?;
    m.add_function(wrap_pyfunction!(gates::apply_pauli_z, m)?)?;
    m.add_function(wrap_pyfunction!(gates::apply_cnot, m)?)?;
    Ok(())
}
