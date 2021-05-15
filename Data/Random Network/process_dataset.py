import pandas as pd
import numpy as np

np.random.seed(1) 

spine_dict = {}
count = 0
df = 0
g = 0

def add_spine_id(row):
    global count
    spine_tuple = (row['cell_index'], row['dendrite_index'], row['spine_index'])
    if spine_tuple in spine_dict.keys():
        spine_id = spine_dict[spine_tuple]
    else:
        count += 1
        spine_dict[spine_tuple] = count
        spine_id = spine_dict[spine_tuple]
    return spine_id

def compute_shape(row):
    shape = (row['shape_1'] - row['shape_2'])/(row['shape_1'] + row['shape_2'])
    return shape

def process_dataset(path):
    df_ = pd.read_csv(path)
    df_.columns = ['cell_index', 'dendrite_index', 'spine_index', 'im_session', 'sipne_I', 'shape_1', 'shape_2', 'dist', 'x_CM', 'y_CM', 'x_den', 'y_den','z_den']
    df_['spine_id'] = df_.apply (lambda row: add_spine_id(row), axis=1)
    df_['shape_param'] = df_.apply (lambda row: compute_shape(row), axis=1)
    return df_

def spine_to_eff(spine_id, session):
    global g
    global df
    index = np.where((df['spine_id'] == spine_id) & (df['im_session'] == session))
    if len(index[0]) == 0:
        y = 0
    else:
        y = df.iloc[index]['shape_param'].mean()*g
    return y

'''
def save_efficacies():
    global df
    global g
    num_spines = df['spine_id'].nunique()
    g = 0.37/df['shape_param'].mean()
    spines = np.arange(1, num_spines + 1)
    sessions = []
    vfunc = np.vectorize(spine_to_eff, otypes=[np.float64])
    for session in range(6):
        session_eff = vfunc(spines, session + 1)
        sessions.append(session_eff)
    sess_to_eff = np.array(sessions)
    sess_to_eff_path = 'sess_to_eff.npy'
    np.save(sess_to_eff_path, sess_to_eff)'''
    
    
def save_efficacies():
    global df
    global g
    num_spines = df['spine_id'].nunique()
    g = [0.37/df[df['session' == session]['shape_param'].mean()
    spines = np.arange(1, num_spines + 1)
    sessions = []
    vfunc = np.vectorize(spine_to_eff, otypes=[np.float64])
    for session in range(6):
        session_eff = vfunc(spines, session + 1)
        sessions.append(session_eff)
    sess_to_eff = np.array(sessions)
    sess_to_eff_path = 'sess_to_eff.npy'
    np.save(sess_to_eff_path, sess_to_eff)



if __name__ == "__main__":
    
    dataset_path = 'publication_data.csv'
    
    df = process_dataset(dataset_path)
    
    save_efficacies()