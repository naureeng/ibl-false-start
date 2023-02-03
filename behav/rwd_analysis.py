"""
RWD_ANALYSIS is reward rate analysis
do mice that make false starts maximize rwd?
author: naureen ghani

"""

import sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.append('/nfs/nhome/live/naureeng/int-brain-lab/ibl-false-start/ephys')
from RT_dist_plot import *
from load_data import *
from plot_utils import *
import pickle

## plot of rwd rate vs % false starts

def running_avg(window, y): 
    ## running average rwd
    average_y = []
    for ind in range(len(y) - window + 1): 
        average_y.append(np.mean(y[ind:ind+window]))
    return average_y

total_rwd = []
prop_fs = []
hit_rate = []

for i in range(len(eids)):
    eid = eids[i]
    try:
        trial = TrialData(eid)
        wheel = WheelData(eid)
        goCueRTs, stimOnRTs, durations = compute_RTs(eid)
    except:
        pass
    goCueRTs = np.array(goCueRTs); stimOnRTs = np.array(stimOnRTs); durations = np.array(durations)

    hr = len(np.argwhere(trial.feedbackType==1)) / len(trial.feedbackType) *100 
    hit_rate.append(hr)

    rwd = sum(trial.rewardVolume)
    fs = len(np.argwhere(goCueRTs<=0.08)) / len(goCueRTs)

    total_rwd.append(rwd / sum(durations))
    prop_fs.append(fs)

    fs_time = np.zeros(len(goCueRTs))
    for i in range(len(goCueRTs)):
        if goCueRTs[i]<=0.08:
            fs_time[i] = 1

    #plt.plot(running_avg(50, np.array(trial.feedbackType)), lw=2)
    #plt.plot(running_avg(50, fs_time), lw=2)

svfg = plt.figure(figsize=(10,8))
plt.scatter(total_rwd, prop_fs, c=hit_rate)
figure_style()
plt.colorbar()
plt.clim([0,100])
svfg.savefig("rwd_rate.png")
print("saved rwd rate plot")

        
