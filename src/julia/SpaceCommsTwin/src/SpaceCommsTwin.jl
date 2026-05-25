module SpaceCommsTwin

using LinearAlgebra
using PyCall
using Optim

export QuantumAnnealing, QAOA_Simulator, VQE_Solver

include("quantum_annealing.jl")
include("qaoa.jl")
include("vqe.jl")
include("utils.jl")

function __init__()
    # Initialize PyCall Python bridge
    @pyimport numpy as np
end

end # module
