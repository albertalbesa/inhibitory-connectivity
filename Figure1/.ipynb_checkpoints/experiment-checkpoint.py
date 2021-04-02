import pandas as pd
import numpy as np
from brian2 import *
from brian2tools import *
from network_generator import NetworkGenerator

np.random.seed(1) 


spine_dict = {}
count = 0
N = 30000
p_EE = 0.51
session = 1
time = 5000*ms


if __name__ == "__main__":
    
    dataset_path = 'publication_data.csv'
    df = process_dataset(dataset_path)

    num_spines = df['spine_id'].nunique()
    g = 0.37/df['shape_param'].mean()
    
    w_EE = generate_weights()
    
    #NG = NetworkGenerator(w_EE)
    #NG.run_network(time)
    
    #process_firings(NG.M_in, NG.M_ex)


    
    