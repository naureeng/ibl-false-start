"""
PROCESS_BEHAV is analysis of mouse-behavior data
author: naureen ghani

"""
import sys
import os
import numpy as np
sys.path.append('/nfs/nhome/live/naureeng/int-brain-lab/ibl-false-start/ephys')
from RT_dist_plot import *

def compute_N_mice(eids):
    ## compute N = #mice from #sessions
    mouse_names = [str(one.eid2path(eid)).split(os.sep)[10] for eid in eids]
    N_mice = len(np.unique(mouse_names))
    subject_names = np.unique(mouse_names)
    return N_mice, mouse_names

def running_avg(window, y):
    ## running average rwd
    average_y = []
    for ind in range(len(y) - window + 1):
        average_y.append(np.mean(y[ind:ind+window]))
    return average_y

def fs_analysis(RTs, i, window):
    ## for a session

    eid_RTs = RTs[i]
    fs_time = np.zeros(len(eid_RTs)); late_time = np.zeros(len(eid_RTs))
    for i in range(len(eid_RTs)):
        if eid_RTs[i]<=0.08:
            fs_time[i] = 1
        if eid_RTs[i]>=1:
            late_time[i] = 1

    fs_rate = running_avg(window, fs_time)
    late_rate = running_avg(window, late_time)

    return fs_rate, late_rate

def fs_mouse(n_eids, hit_rate, RTs, window):
    ## for a mouse

    fs_eids = []; late_eids = []
    for n in range(n_eids):
        fs_rate, late_rate = fs_analysis(RTs, n, window)
        if hit_rate[n] >= 85:
            fs_eids.append(fs_rate); late_eids.append(late_rate)

    return fs_eids, late_eids

## [2] process data
def build_pyschometric_dict(eids, RT_type):
    """ 
    eids: sessions [string]
    RT_type: "posRT" or "negRT" [string]
    """

    eid_count = 0
    keyList = {"80_fracR", "20_fracR", "50_fracR", "80_total", "20_total", "50_total"}
    data = {key: None for key in keyList}

    ## [2] process data
    data_80fracR = []; data_20fracR = []; data_50fracR = []
    data_80total = []; data_20total = []; data_50total = []

    for i in range(len(eids)):
        eid = eids[i]
        print(eid)
        try:
            trials = TrialData(eid)
            wheel = WheelData(eid)
        except:
            continue
        wheel.calc_trialwise_wheel(trials.stimOn_times, trials.feedback_times)
        wheel.calc_movement_onset_times(trials.stimOn_times)

        wheel.calc_trialwise_wheel(trials.stimOn_times, trials.feedback_times)
        wheel.calc_movement_onset_times(trials.stimOn_times)
        RTs = wheel.first_movement_onset_times - trials.stimOn_times
        false_start_threshold = 0.08 # [sec]
        trials.psychometric_curve(wheel.first_movement_directions, RTs, false_start_threshold)

        if RT_type=="negRT":
            a = 1
        else:
            a = 0

        ## left block [80/20]
        data_80fracR.append(np.nan_to_num(trials.fraction_choice_right[a][0][:]))
        data_80total.append(np.nan_to_num(trials.performance_cnts[a][0][:]))

        ## right block [20/80]
        data_20fracR.append(np.nan_to_num(trials.fraction_choice_right[a][1][:]))
        data_20total.append(np.nan_to_num(trials.performance_cnts[a][1][:]))

        ## unbiased block [50/50]
        data_50fracR.append(np.nan_to_num(trials.fraction_choice_right[a][2][:]))
        data_50total.append(np.nan_to_num(trials.performance_cnts[a][2][:]))

        eid_count += 1

    print(f"n={eid_count} sessions")

    ## store eids to dict
    keyList = {"80_fracR", "20_fracR", "50_fracR", "80_total", "20_total", "50_total"}
    data["80_fracR"] = data_80fracR; data["20_fracR"] = data_20fracR; data["50_fracR"] = data_50fracR
    data["80_total"] = data_80total; data["20_total"] = data_20total; data["50_total"] = data_50total

    return data


