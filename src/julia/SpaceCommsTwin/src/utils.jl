module QuantumUtils

using LinearAlgebra
import PyCall

export pauli_matrices, tensor_product, random_quantum_state, state_fidelity

const σx = [0.0 1.0; 1.0 0.0]
const σy = [0.0 -1.0im; 1.0im 0.0]
const σz = [1.0 0.0; 0.0 -1.0]
const I2 = [1.0 0.0; 0.0 1.0]

function pauli_matrices()
    return (I2, σx, σy, σz)
end

function tensor_product(A::Matrix, B::Matrix)::Matrix
    return kron(A, B)
end

function random_quantum_state(n::Int)::Vector{ComplexF64}
    state = randn(ComplexF64, 2^n) + 1.0im * randn(ComplexF64, 2^n)
    return state / norm(state)
end

function state_fidelity(psi::Vector{ComplexF64}, phi::Vector{ComplexF64})::Float64
    return abs(dot(psi, phi))^2
end

end
