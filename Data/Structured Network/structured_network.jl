using Random
using Distributions
using LinearAlgebra
using DelimitedFiles
using SparseArrays


f = 0.1
N = 40000
N_I = Int64(0.2*N)
P = 2000
d_normal = Normal()
z_norm = convert(Float32, sqrt(2)/(f*(1-f)*sqrt(P)))


function compute_amp(W, W2)
    return convert(Float32, W^2/sqrt(W2))
end


function compute_logvar(W, W2)
    return convert(Float32, sqrt(log(W2/W^2)))
end

function compute_eff_e(z::Float32, psi::Float32, logvar::Float32, c::Float32, cum::Float32, amp::Float32)
    if z <= psi
        return 0
    else
        y = (cdf(d_normal, z) - cum)/c
        phi = quantile.(d_normal, y)
        out = amp*exp(phi*logvar)
        out = convert(Float32, out)
        return out
    end
end

function compute_eff_i(z::Float32, psi::Float32, logvar::Float32, c::Float32, cum::Float32, amp::Float32)
    if -z <= psi
        return 0
    else
        y = (1 - cum - cdf(d_normal, z))/c
        phi = quantile.(d_normal, y)
        out = amp*exp(phi*logvar)
        out = convert(Float32, out)
        return out
    end
end


c_EE = Float32(0.2)
c_IE = Float32(0.3)
c_EI = Float32(0.4)
c_II = Float32(0.4)
psi_EE = convert(Float32, quantile.(d_normal, (1 - c_EE)))
psi_IE = convert(Float32, quantile.(d_normal, (1 - c_IE)))
psi_EI = convert(Float32, quantile.(d_normal, (1 - c_EI)))
psi_II = convert(Float32, quantile.(d_normal, (1 - c_II)))
W_EE = 0.37
W_IE = 0.66
W_EI = 0.44
W_II = 0.54
W_EE2 = 0.26
W_IE2 = 0.65
W_EI2 = 0.49
W_II2 = 0.53
amp_EE = compute_amp(W_EE, W_EE2)
amp_IE = compute_amp(W_IE, W_IE2)
amp_EI = compute_amp(W_EI, W_EI2)
amp_II = compute_amp(W_II, W_II2)
logvar_EE = compute_logvar(W_EE, W_EE2)
logvar_IE = compute_logvar(W_IE, W_IE2)
logvar_EI = compute_logvar(W_EI, W_EI2)
logvar_II = compute_logvar(W_II, W_II2)
cum_EE = 1 - c_EE
cum_IE = 1 - c_IE
cum_EI = 1 - c_EI
cum_II = 1 - c_II


bern_f = Bernoulli(f)
p_epsilon = 1/sqrt(2)
bern_e = Bernoulli(p_epsilon)


println("generating patterns...")
patterns = rand(bern_f, N, P)
writedlm("patterns.csv", patterns, ',')
patterns = readdlm("patterns.csv", ',')

reduced_patterns = patterns .- f
epsilon_i = rand(bern_e, N, P)
epsilon_j = rand(bern_e, N, P)
reduced_i = convert(Matrix{Float32}, epsilon_i.*reduced_patterns)
reduced_j = convert(Matrix{Float32}, epsilon_j.*reduced_patterns)

println("computing z matrix...")
z = reduced_i * transpose(reduced_j)

z = z_norm.*z

println("computing w_EE...")
w_EE = z[(N_I + 1):end, (N_I + 1):end]
w_EE = map(z -> compute_eff_e(z, psi_EE, logvar_EE, c_EE, cum_EE, amp_EE), w_EE)
writedlm("w_EE_struct.csv", w_EE, ',')

println("computing w_IE...")
w_IE = z[1:N_I, (N_I + 1):end]
w_IE = map(z -> compute_eff_e(z, psi_IE, logvar_IE, c_IE, cum_IE, amp_IE), w_IE)
writedlm("w_IE_struct.csv", w_IE, ',')

println("computing w_EI...")
w_EI = z[(N_I + 1):end, 1:N_I]
w_EI = map(z -> compute_eff_i(z, psi_EI, logvar_EI, c_EI, cum_EI, amp_EI), w_EI)
writedlm("w_EI_struct.csv", w_EI, ',')


println("computing w_II...")
w_II = z[1:N_I, 1:N_I]
w_II = map(z -> compute_eff_i(z, psi_II, logvar_II, c_II, cum_II, amp_II), w_II)
writedlm("w_II_struct.csv", w_II, ',')

println("completed!")