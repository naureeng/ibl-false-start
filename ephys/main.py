"""
MAIN is master script 
author: naureen ghani

"""
from load_data import *
from process_data import *
from save_data import *

## [1] load 
eid, probe = load_eid("ACA", "L", 0)
trials, wheel, d_pos, d_neg, d_zero = obtain_wheel(eid, probe, "L")
pos_final, neg_final, zero_final = obtain_neural(eid, probe, d_pos, d_neg, d_zero, "ACA") 

## [2] process
get_neural_unit(pos_final, neg_final, zero_final, 0.02, 1)

## [3] save
plot_unit(1, "motionOnset", "#004F98", "#EE2E31", "grey")
