module QuantumAnnealing

using LinearAlgebra

export IsingHamiltonian, annealing_schedule, simulate_annealing

struct IsingHamiltonian
    h::Vector{Float64}
    J::Matrix{Float64}
end

function IsingHamiltonian(n::Int)
    IsingHamiltonian(zeros(n), zeros(n, n))
end

function energy(H::IsingHamiltonian, spin_config::Vector{Int})::Float64
    E = 0.0
    for i in 1:length(H.h)
        E -= H.h[i] * spin_config[i]
    end
    for i in 1:length(H.h)
        for j in (i+1):length(H.h)
            E -= H.J[i, j] * spin_config[i] * spin_config[j]
        end
    end
    return E
end

function annealing_schedule(t::Float64, total_time::Float64)::Tuple{Float64, Float64}
    s = t / total_time
    A = 1.0 - s
    B = s
    return A, B
end

function simulate_annealing(H_final::IsingHamiltonian, n_steps::Int; T::Float64=1.0)
    n = length(H_final.h)
    spins = rand([-1, 1], n)
    energies = Float64[]

    for step in 1:n_steps
        i = rand(1:n)
        ΔE = 2.0 * H_final.h[i] * spins[i]
        for j in 1:n
            if j != i
                ΔE += 2.0 * H_final.J[i, j] * spins[i] * spins[j]
            end
        end
        if ΔE < 0.0 || rand() < exp(-ΔE / T)
            spins[i] = -spins[i]
        end
        push!(energies, energy(H_final, spins))
    end

    return spins, energies
end

end
