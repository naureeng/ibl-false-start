"""
LOAD_BEHAV is load functions for behavioral data
author: naureen ghani

"""

import sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.append('/nfs/nhome/live/naureeng/int-brain-lab/ibl-false-start/ephys')
from RT_dist_plot import *
from load_data import *
import pickle

def obtain_mouse_behav(subject_name):
    eids = one.search(subject=subject_name)
    print(len(eids), "sessions")

    rwd_rate = []; prop_fs = []; hit_rate = []; hit_rate_hi = []; total_rwd = []; total_trials = []; RTs = []
    for i in range(len(eids)):
        eid = eids[i]
        try:
            trial = TrialData(eid)
            wheel = WheelData(eid)
            goCueRTs, stimOnRTs, durations = compute_RTs(eid)
        except:
            continue
        goCueRTs = np.array(goCueRTs); stimOnRTs = np.array(stimOnRTs); durations = np.array(durations)
        RTs.append(stimOnRTs)

        #hr = len(np.argwhere(trial.feedbackType==1)) / len(trial.feedbackType) *100

        ## build contrast array
        n_trials = trial.total_trial_count
        print(n_trials, "trials")

        trial.contrast = np.empty(n_trials)
        contrastRight_idx = np.where(~np.isnan(trial.contrastRight))[0]
        contrastLeft_idx = np.where(~np.isnan(trial.contrastLeft))[0]

        trial.contrast[contrastRight_idx] = trial.contrastRight[contrastRight_idx]
        trial.contrast[contrastLeft_idx] = -1 * trial.contrastLeft[contrastLeft_idx]

        ## psychometric
        overall_hr = len(np.argwhere(trial.feedbackType==1)) / len(trial.feedbackType) *100
        hit_rate.append(overall_hr)
        contrast_values = np.unique(trial.contrast)

        ## initialize hit_rate_value to plot
        hr = []

        for i in range(len(contrast_values)):
            idx = np.argwhere(trial.contrast==contrast_values[i])
            val = len (np.argwhere(trial.feedbackType[idx]==1)) / len(idx) *100
            hr.append(val)

        hit_rate_hi.append((hr[0]+hr[-1])/2)

        rwd = sum(trial.rewardVolume)
        fs = len(np.argwhere(goCueRTs<=0.08)) / len(goCueRTs)

        total_rwd.append(rwd)
        rwd_rate.append(rwd / sum(durations))
        prop_fs.append(fs)
        total_trials.append(trial.total_trial_count)

        fs_time = np.zeros(len(goCueRTs))
        for i in range(len(goCueRTs)):
            if goCueRTs[i]<=0.08:
                fs_time[i] = 1

    ## store data as pkl
    f = open(f'{subject_name}.behav', 'wb')
    pickle.dump([rwd_rate, prop_fs, hit_rate, hit_rate_hi, total_rwd, total_trials, RTs], f)
    f.close()

