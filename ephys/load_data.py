"""
LOAD_DATA stores wheel and neural data per eid
author: naureen ghani

"""

import numpy as np
from RT_dist_plot import *
from wheel_utils import *
from ephys_utils import *

def load_eid(reg, side, n):
    """
    reg:     region [string]
    side:    "L" or "R" [string] 
    n:       session num [int]
    """
    eids = np.load(f"/nfs/gatsbystor/naureeng/{reg}/{side}_eids_all.npy")
    probes = np.load(f"/nfs/gatsbystor/naureeng/{reg}/{side}_probes_all.npy")
    print(len(eids), f"{side}-movement sessions")

    eid = eids[n]
    probe = probes[n]
    print(eid)

    return eid, probe

def obtain_wheel(eid, probe, side):
    trials = TrialData(eid)
    wheel  = WheelData(eid)
    d_left, d_neg_left, d_right, d_neg_right, d_zero_left, d_zero_right, trial_time_all, trial_position_all, trial_velocity_all = get_extended_trial_windows(eid, 0.08, 0.12, 1, -1, 1, 60, "ballistic")

    if side=="L":
        d_pos = d_left; d_neg = d_neg_left; d_zero = d_zero_left
    else:
        d_pos = d_right; d_neg = d_neg_right; d_zero = d_zero_right

    return trials, wheel, d_pos, d_neg, d_zero

def obtain_neural(eid, probe, d_pos, d_neg, d_zero, reg):
    Res_pos,  noisy_pos  = pair_firing_rate_contrast(eid, probe, d_pos, reg, -1, 1, 0.02, "motionOnset")
    Res_neg,  noisy_neg  = pair_firing_rate_contrast(eid, probe, d_neg, reg, -1, 1, 0.02, "motionOnset")
    Res_zero, noisy_zero = pair_firing_rate_contrast(eid, probe, d_zero, reg, -1, 1, 0.02, "motionOnset")
    pos_final, neg_final, zero_final = remove_noisy_units(Res_pos, noisy_pos, Res_neg, noisy_neg, Res_zero, noisy_zero)
    print(pos_final.shape)
    print(neg_final.shape)
    print(zero_final.shape)

    return pos_final, neg_final, zero_final



