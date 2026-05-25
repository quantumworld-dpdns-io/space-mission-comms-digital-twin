module QAOA_Simulator

using LinearAlgebra

export maxcut_hamiltonian, qaoa_circuit, compute_expectation

function maxcut_hamiltonian(edges::Vector{Tuple{Int,Int}}, n::Int)::Matrix{Float64}
    H = zeros(Float64, 2^n, 2^n)
    for (i, j) in edges
        term = zeros(Float64, 2^n, 2^n)
        for k in 0:(2^n - 1)
            bits = digits(k, base=2, pad=n)
            bits[i+1] = 1 - bits[i+1]
            l = sum(bits[t] * (1 << (t-1)) for t in 1:n)
            term[k+1, l+1] = 1.0
        end
        H += term
    end
    return H
end

function qaoa_circuit(gamma::Float64, beta::Float64, n::Int, edges::Vector{Tuple{Int,Int}})
    return gamma, beta, n, edges
end

function compute_expectation(H::Matrix{Float64}, state::Vector{ComplexF64})::Float64
    H_state = H * state
    return real(dot(state, H_state))
end

end
