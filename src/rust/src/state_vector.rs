use ndarray::Array1;
use num_complex::Complex64;
use pyo3::prelude::*;
use rayon::prelude::*;

#[pyclass]
pub struct StateVector {
    amplitude: Array1<Complex64>,
    num_qubits: usize,
    dimension: usize,
}

#[pymethods]
impl StateVector {
    #[new]
    pub fn new(num_qubits: usize) -> Self {
        let dimension = 1 << num_qubits;
        let mut amplitude = Array1::zeros(dimension);
        amplitude[0] = Complex64::new(1.0, 0.0);
        StateVector {
            amplitude,
            num_qubits,
            dimension,
        }
    }

    pub fn get_amplitude(&self, index: usize) -> Complex64 {
        self.amplitude[index]
    }

    pub fn get_num_qubits(&self) -> usize {
        self.num_qubits
    }

    pub fn probability(&self, index: usize) -> f64 {
        let amp = self.amplitude[index];
        amp.norm_sqr()
    }

    pub fn measure(&mut self) -> usize {
        let probs: Vec<f64> = (0..self.dimension)
            .map(|i| self.amplitude[i].norm_sqr())
            .collect();

        let r: f64 = rand::random();
        let mut cumulative = 0.0;
        for i in 0..self.dimension {
            cumulative += probs[i];
            if r < cumulative {
                let mut new_state = Array1::zeros(self.dimension);
                new_state[i] = Complex64::new(1.0, 0.0);
                self.amplitude = new_state;
                return i;
            }
        }
        0
    }

    pub fn apply_gate(&mut self, gate_matrix: Vec<Vec<Complex64>>, target_qubit: usize) {
        let dim = 1 << self.num_qubits;
        let mut new_state = Array1::zeros(dim);

        for i in 0..dim {
            let bit = (i >> target_qubit) & 1;
            let pair_i = if bit == 0 { i } else { i ^ (1 << target_qubit) };

            for j in 0..2 {
                let input_i = if j == 0 { i } else { i ^ (1 << target_qubit) };
                let g = if bit == 0 {
                    gate_matrix[j][0]
                } else {
                    gate_matrix[j][1]
                };
                new_state[i] += g * self.amplitude[input_i];
            }
        }
        self.amplitude = new_state;
    }

    pub fn apply_two_qubit_gate(
        &mut self,
        gate_matrix: Vec<Vec<Complex64>>,
        control: usize,
        target: usize,
    ) {
        let dim = self.dimension;
        let mut new_state = Array1::zeros(dim);

        for i in 0..dim {
            let c_bit = (i >> control) & 1;
            let t_bit = (i >> target) & 1;
            let input_state = if c_bit == 1 {
                i ^ (1 << target)
            } else {
                i
            };

            let row = (c_bit << 1) | t_bit;
            let col = (c_bit << 1) | (if c_bit == 1 { 1 - t_bit } else { t_bit });
            new_state[i] = gate_matrix[row][col] * self.amplitude[input_state];
        }
        self.amplitude = new_state;
    }
}
