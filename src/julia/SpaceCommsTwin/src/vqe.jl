module VQE_Solver

using LinearAlgebra
using Optim

export hamiltonian_from_pauli, create_ansatz, minimize_expectation

function hamiltonian_from_pauli(pauli_terms::Vector{Tuple{Vector{Char}, Float64}}, n::Int)::Matrix{Float64}
    H = zeros(Float64, 2^n, 2^n)
    I2 = [1.0 0.0; 0.0 1.0]
    X = [0.0 1.0; 1.0 0.0]
    Y = [0.0 -1.0im; 1.0im 0.0]
    Z = [1.0 0.0; 0.0 -1.0]

    for (ops, coeff) in pauli_terms
        term = 1.0
        for op in ops
            if op == 'I'
                term = kron(term, I2)
            elseif op == 'X'
                term = kron(term, X)
            elseif op == 'Y'
                term = kron(term, Y)
            elseif op == 'Z'
                term = kron(term, Z)
            end
        end
        H += coeff * real(term)
    end

    return H
end

function create_ansatz(n::Int)::Function
    function ansatz(params::Vector{Float64})
        state = zeros(ComplexF64, 2^n)
        state[1] = 1.0
        return state
    end
    return ansatz
end

function minimize_expectation(H::Matrix{Float64}, n::Int; method=BFGS())
    ansatz = create_ansatz(n)

    function energy(params::Vector{Float64})
        state = ansatz(params)
        return real(dot(state, H * state))
    end

    result = optimize(energy, zeros(n * 2), method)
    return result.minimum, result.minimizer
end

end
