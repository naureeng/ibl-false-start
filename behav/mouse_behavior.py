"""
MOUSE_BEHAVIOR is master script for behavioral analysis
author: naureen ghani

"""
import numpy as np
import matplotlib.pyplot as plt
from load_behav import *
from plot_behav import *
import pickle
import pandas as pd
import os


df = pd.read_excel('expert_mouse.xlsx')
print(len(df), "expert mice")

for i in range(len(df)):
    subject_name = df["subject_name"][i]
    try:
        if not os.path.exists(f"/nfs/gatsbystor/naureeng/expert_mouse/{subject_name}/"):
            os.makedirs(f"/nfs/gatsbystor/naureeng/expert_mouse/{subject_name}/")

    ## [1] load data
        obtain_mouse_behav(subject_name)

        ## [2] process data
        f = open(f'{subject_name}.behav', 'rb')
        rwd_rate, prop_fs, hit_rate, hit_rate_hi, total_rwd, total_trials, RTs = pickle.load(f)
        f.close()

        ## [3] plot data
        n_eids = len(hit_rate)
        fs_eids, late_eids = fs_mouse(n_eids, hit_rate, RTs, 100)
        fs_mean, fs_error, late_mean, late_error = plot_mouse_position(subject_name, fs_eids, late_eids, n_eids)
        print("saved mouse position plot")

        plot_mouse_rate(subject_name, total_rwd, prop_fs, hit_rate)
        print("saved mouse rwd rate plot")

        print(rwd_rate)
        print(np.median(np.nan_to_num(rwd_rate)))

        ## [4] store data
        np.savez_compressed(f"/nfs/gatsbystor/naureeng/expert_mouse/{subject_name}/fs_mean.npz", data=fs_mean.data, mask=fs_mean.mask)
        np.savez_compressed(f"/nfs/gatsbystor/naureeng/expert_mouse/{subject_name}/fs_error.npz", data=fs_error.data, mask=fs_error.mask)
        np.savez_compressed(f"/nfs/gatsbystor/naureeng/expert_mouse/{subject_name}/late_mean.npz", data=late_mean.data, mask=late_mean.mask)
        np.savez_compressed(f"/nfs/gatsbystor/naureeng/expert_mouse/{subject_name}/late_error.npz", data=late_error.data, mask=late_error.mask)
        np.save(f"/nfs/gatsbystor/naureeng/expert_mouse/{subject_name}/median_rwd_rate.npy", np.median(np.nan_to_num(rwd_rate)))
        np.save(f"/nfs/gatsbystor/naureeng/expert_mouse/{subject_name}/median_prop_fs.npy", np.median(np.nan_to_num(prop_fs)))
        np.save(f"/nfs/gatsbystor/naureeng/expert_mouse/{subject_name}/median_hit_rate.npy", np.median(np.nan_to_num(hit_rate)))
    except:
        continue

    ## sanity check
    #with np.load(f"/nfs/gatsbystor/naureeng/expert_mouse/{subject_name}/fs_mean.npz") as npz:
        #arr = np.ma.MaskedArray(**npz)
        #print(arr)

    #print(np.load(f"/nfs/gatsbystor/naureeng/expert_mouse/{subject_name}/median_prop_fs.npy"))

#plot_session_position(RTs, 7, 100)
#print("saved session position plot")
