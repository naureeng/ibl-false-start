"""
author: naureen ghani
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
from itertools import compress
import pickle

## plot #trials since block switch vs fraction of rightward trials, separated by left vs right blocks

eidData = pd.read_csv("eid_behav_qc_analysis.csv")

T_BIN = 4 ## [units = #trials]

def compute_blk_change_choice(df, blk_value):
    data = []
    for i in np.arange(1,100,T_BIN):

        df_g = df.query(f'block=={blk_value} & RT<=0 & RT>=-0.20 & trials_blk_change>={i} & trials_blk_change<={i+T_BIN}').head()

        n_trials_bin = df_g[df_g.columns[0]].count()
        val = df_g.query("choice==1") 
        n_trials_right = val[val.columns[0]].count()

        totalData = (n_trials_right / n_trials_bin)
        data.append(totalData)
    
    ## compute t = 0 separately
    df_z = df.query(f'block=={blk_value} & RT<=0 & RT>=-0.20 & trials_blk_change==0').head()
    n_trials_z = df_z[df_z.columns[0]].count()
    val_z = df_z.query("choice==1") 
    n_right_z = val_z[val_z.columns[0]].count()

    ## full data
    data.insert(0, n_right_z / n_trials_z)

    return data

svfg = plt.figure(figsize=(10,8))
plt.rcParams['font.sans-serif'] = "Arial"
plt.rcParams['font.family'] = "sans-serif"
plt.rcParams['xtick.labelsize'] = 20
plt.rcParams['ytick.labelsize'] = 20
plt.rcParams["axes.linewidth"] = 2

right_blk  = compute_blk_change_choice(eidData, 0.2) 
left_blk  = compute_blk_change_choice(eidData, 0.8) 

subjects = pd.Series(eidData["eid"].values.ravel()).unique().tolist()
subjects.sort()

print(len(subjects), "sessions")

rightData = []; leftData = [];  
for i in range(len(subjects)):
    subject = subjects[i]
    sub_data = eidData.loc[(eidData["eid"] == subject)]
    right_eid.append(compute_blk_change_choice(sub_data, 0.2))
    left_eid, z_L = compute_blk_change_choice(sub_data, 0.8)

## pickle data
f = open('falsestart.blockchange', 'wb')
pickle.dump([rightData, leftData], f)
f.close()
print("data pickled")
