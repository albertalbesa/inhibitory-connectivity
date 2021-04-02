from brian2 import *
import time
from brian2tools import *
import numpy as np



#this function takes as input the first and second momentum of the weights population given in supp table 1 
#it transforms the average and var into the average and std of a lognormal distribution (formulas taken from wikipedia)
def process_params(av, av2):
    var = (av2 - av**2)
    
    mu = np.log(av**2/(av**2 + var)**(1/2))
    sigma = np.log(1 + var/av**2)
    
    return mu, sigma



#the weight distribution parameters are processed and stored in non-array variables to be passed to brian
#in the future let's just do this computation and store the values in a file to read
avs = np.array([0.37, 0.66, 0.44, 0.54])
avs2 = np.array([0.26, 0.65, 0.49, 0.53])
lognormal_mu = []
lognormal_std = []
for i in range(len(avs)):
    mu, sigma = process_params(avs[i], avs2[i])
    lognormal_mu.append(mu)
    lognormal_std.append(sigma) 
ee_mu = lognormal_mu[0]
ee_std = lognormal_std[0]
ie_mu = lognormal_mu[1]
ie_std = lognormal_std[1]
ei_mu = lognormal_mu[2]
ei_std = lognormal_std[2]
ii_mu = lognormal_mu[3]
ii_std = lognormal_std[3]



class NetworkGenerator():
    def __init__(self, w_EE = 0):
        
        self.W_EE = w_EE
        
        self.M_in = 0
        self.M_ex = 0
        
    def run_network(self, total_time):

        #total size of the network
        N = 40000

        #threshold, reset and refractory parameters
        v_theta = 33*mV
        v_reset = 24.75*mV
        tau_ref = 1*ms
        v_0 = -1000*mV

        #indices that delimit inhibitory and excitatory populations 20/80
        first_inh = 0
        last_inh = int(0.2*N)
        first_exc = last_inh
        last_exc = N

        g_E = 1
        g_I = 1

        #External drive to each population
        H_in = 57.8*mV
        H_ex = 77.6*mV
        initial_v = np.load('initial_voltage.npy')

        #clear brian scope to reset any past variables
        start_scope()

        #define the model that each neuron will follow
        tau = 10*ms
        eqs = '''
        dv/dt = -(v - H)/tau : volt (unless refractory)
        H : volt
        '''

        #the original network is defined
        all_neurons = NeuronGroup(N, eqs, threshold = 'v>v_theta', reset = 'v=v_reset', refractory = tau_ref, method = 'exact')

        #to work with subpopulations bria-n uses slicing notation
        in_neurons = all_neurons[first_inh:last_inh]
        ex_neurons = all_neurons[first_exc:last_exc]

        all_neurons.v = initial_v*mV


        #define external drive according to supp table 1
        in_neurons.H = H_in
        ex_neurons.H = H_ex

        #initialize the synaptic object for the different subpopulation pairs
        S_EE = Synapses(ex_neurons, ex_neurons, 'w : volt', on_pre ='v += w')
        S_IE = Synapses(ex_neurons, in_neurons, 'w : volt', on_pre ='v += w')
        S_EI = Synapses(in_neurons, ex_neurons,'w : volt', on_pre ='v -= w')
        S_II = Synapses(in_neurons, in_neurons, 'w : volt', on_pre ='v -= w')

        #connect them according to probabilities in supp table 1
        S_EE.connect(p = 0.2)
        S_IE.connect(p = 0.3)
        S_EI.connect(p = 0.4)
        S_II.connect(p = 0.4)

        #distribute them log-normal according to parameters obtained in processing cells (beginning of notebook)
        S_EE.w = 'g_E*exp(ee_mu + ee_std*randn())*mV'
        S_IE.w = 'g_E*exp(ie_mu + ie_std*randn())*mV'
        S_EI.w = 'g_I*exp(ei_mu + ei_std*randn())*mV'
        S_II.w = 'g_I*exp(ii_mu + ii_std*randn())*mV'

        #define monitoring variables. these can monitor the whole population or a desired subpopulation
        #monitors spiking events
        M_in = SpikeMonitor(in_neurons)
        M_ex = SpikeMonitor(ex_neurons)
        
        
        defaultclock.dt = 0.005*ms

        run(total_time, report = 'text')
        
        self.M_in = M_in
        self.M_ex = M_ex