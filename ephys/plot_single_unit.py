"""
PLOT_SINGLE_UNIT plots one neuron
author: naureen ghani
"""

from wheel_utils import *
from ephys_utils import *
import numpy as np

## [1] load 
reg = "ACA"
eids = np.load(f"/nfs/gatsbystor/naureeng/{reg}/L_eids_all.npy")
probes = np.load(f"/nfs/gatsbystor/naureeng/{reg}/L_probes_all.npy")
print(len(eids), "left-movement sessions")

i = 0
eid = eids[i]
probe = probes[i]
print(eid)

# obtain wheel data 
d_left, d_neg_left, d_right, d_neg_right, d_zero_left, d_zero_right, trial_time_all, trial_position_all, trial_velocity_all = get_extended_trial_windows(eid, 0.08, 0.12, 1, -1, 1, 60, "ballistic") 

# obtain neural data
def obtain_neural(eid, probe, d_pos, d_neg, d_zero, reg):
    Res_pos,  noisy_pos  = pair_firing_rate_contrast(eid, probe, d_pos, reg, -1, 1, 0.02, "motionOnset")
    Res_neg,  noisy_neg  = pair_firing_rate_contrast(eid, probe, d_neg, reg, -1, 1, 0.02, "motionOnset")
    Res_zero, noisy_zero = pair_firing_rate_contrast(eid, probe, d_zero, reg, -1, 1, 0.02, "motionOnset")
    pos_final, neg_final, zero_final = remove_noisy_units(Res_pos, noisy_pos, Res_neg, noisy_neg, Res_zero, noisy_zero)
    print(pos_final.shape)
    print(neg_final.shape)
    print(zero_final.shape)

    return pos_final, neg_final, zero_final

pos_left, neg_left, zero_left    = obtain_neural(eid, probe, d_left, d_neg_left, d_zero_left, reg)
pos_right, neg_right, zero_right = obtain_neural(eid, probe, d_right, d_neg_right, d_zero_right, reg)

## [2] process

## [3] save


