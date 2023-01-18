"""
MAIN is master script 
author: naureen ghani

"""
from load_data import *
from process_data import *
from save_data import *
import logging

## parameters
brain_reg = ["VISp", "VISl", "VISpm", "VISam", "VISa", "AUD", "RSP", "ACA", "MOs", "PL", "ILA", "ORB", "MOp", "SSp",
        "DG", "CA3", "CA1", "POST", "OLF", "CP", "GP", "SNr", "ACB" , "LS", "LG", "LP", "LD",  
        "MD", "VPL", "PO", "VPM", "RT", "MG", "SC", "MRN", "APN", "PAG", "ZI"] 

side = "R"

for i in range(len(brain_reg)):

    ## [1] load
    reg = brain_reg[i]
    _, _, n_eids = load_eid(reg, side, 0)

    ## [2] process
    st_mat = []; fs_mat = []; ze_mat = [] ## st=stimulus-triggered; fs=false-start; ze=zero
    for n in range(n_eids):
        eid, probe, _ = load_eid(reg, side, n)
        trials, wheel, d_pos, d_neg, d_zero = obtain_wheel(eid, probe, side)

        try:
            pos_final, neg_final, zero_final = obtain_neural(eid, probe, d_pos, d_neg, d_zero, reg) 
            ## [2] process and [3] save single-unit plots
            n_units = len(pos_final)
            for n in range(n_units):
                pos_unit, neg_unit, zero_unit = get_neural_unit(pos_final, neg_final, zero_final, 0.02, n)
                #plot_unit(n, "motionOnset", "#004F98", "#EE2E31", "grey")
                st_mat.append(pos_unit); fs_mat.append(neg_unit); ze_mat.append(zero_unit)
        except:
            logging.warning("eid issue")
            pass

    ## append one row to separate regions in plot
    #listofzeros = [0] * 100
    #st_mat.append(listofzeros); fs_mat.append(listofzeros); ze_mat.append(listofzeros)

    st_mat = np.array(st_mat); fs_mat = np.array(fs_mat); ze_mat = np.array(ze_mat)
    print(st_mat.shape); print(fs_mat.shape); print(ze_mat.shape)

    ## store data as pkl
    f = open('neural.data', 'wb')
    pickle.dump([st_mat, fs_mat, ze_mat], f)
    f.close()

    plot_psth(reg, side)
