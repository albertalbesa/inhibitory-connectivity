using Random
using Distributions
using NPZ
using StatsBase
using DelimitedFiles

N = 30000
p_EE = 0.51
num_sessions = 6
num_spines = 3688

sess_to_eff = npzread("sess_to_eff.npy")


session_dicts = []
for session = 1:num_sessions
    sess = sess_to_eff[session, :]
    session_dict = Dict()
    for (index, value) in enumerate(session_dict)
        session_dict[index] = value
    push!(session_dicts, session_dict)
    end
end

function assign_spine(x::Integer)
    if x == 1
        y = rand(1:num_spines)
    else
        y = 0
    end
    return y
end

function assign_eff(spine_id::Int64, session::Int64)
    if spine_id == 0
        return spine_id
    else
        return sess_to_eff[session, spine_id]
    end
end

function assign_eff_dict(spine_id::Int64, session::Int64)
    if spine_id == 0
        return spine_id
    else
        return session_dicts[session][spine_id]
    end
end


d = Bernoulli(p_EE)
w_rand = rand(d, N^2)
w_spine = map(assign_spine, w_rand)


println("computing w_EE for session 1...")
w_EE1 = map(spine_id -> assign_eff(spine_id, 1), w_spine)
writedlm( "w_EE1.csv", w_EE1, ',')

println("computing w_EE for session 2...")
w_EE2 = map(spine_id -> assign_eff(spine_id, 2), w_spine)
writedlm( "w_EE2.csv", w_EE2, ',')

println("computing w_EE for session 3...")
w_EE3 = map(spine_id -> assign_eff(spine_id, 3), w_spine)
writedlm( "w_EE3.csv", w_EE3, ',')

println("computing w_EE for session 4...")
w_EE4 = map(spine_id -> assign_eff(spine_id, 4), w_spine)
writedlm( "w_EE4.csv", w_EE4, ',')

println("computing w_EE for session 5...")
w_EE5 = map(spine_id -> assign_eff(spine_id, 5), w_spine)
writedlm( "w_EE5.csv", w_EE5, ',')

println("computing w_EE for session 6...")
w_EE6 = map(spine_id -> assign_eff(spine_id, 6), w_spine)
writedlm( "w_EE6.csv", w_EE6, ',')