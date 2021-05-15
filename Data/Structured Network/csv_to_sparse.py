from scipy.io import savemat
from scipy import sparse
import pandas as pd
import numpy as np


N_E = 32000
N_I = 8000

df = pd.read_csv('w_EE_struct.csv', header = None)
w_EE = np.array(df.values).reshape(N_E, N_E)
w_EE = sparse.csc_matrix(w_EE)
sparse.save_npz('w_IE_sparse.npz', w_EE)

df = pd.read_csv('w_IE_struct.csv', header = None)
w_IE = np.array(df.values).reshape(N_I, N_E)
w_IE = sparse.csc_matrix(w_IE)
sparse.save_npz('w_IE_sparse.npz', w_IE)

df = pd.read_csv('w_EI_struct.csv', header = None)
w_EI = np.array(df.values).reshape(N_E, N_I)
w_EI = sparse.csc_matrix(w_EI)
sparse.save_npz('w_EI_sparse.npz', w_EI)

df = pd.read_csv('w_II_struct.csv', header = None)
w_II = np.array(df.values).reshape(N_I, N_I)
w_II = sparse.csc_matrix(w_II)
sparse.save_npz('w_II_sparse.npz', w_II)