"""
PROCESS_DATA is pre-processing neural data analysis
author: naureen ghani

"""
import numpy as np
import pickle
from scipy.stats import sem, zscore

def process_unit(data, T_BIN, n):
    spikes = data[n,:,:]
    unit = np.mean(spikes,axis=1)/T_BIN
    _, trials = spikes.shape

    ## compute baseline
    pre_bin = int((1-0.5)/0.02)
    post_bin = int((1-0) /0.02)
    baseline = np.mean(unit[pre_bin:post_bin])

    ## subtract baseline
    corr = unit - baseline

    ## zscore
    unit_final = zscore(corr)
    unit_error = sem(corr)

    ## 95th percentile confidence interval
    ci = 1.96 * np.std(spikes, axis=1)/np.sqrt(trials)

    return unit_final, unit_error, ci, trials

def get_neural_unit(pos_final, neg_final, zero_final, T_BIN, n):
    pos_unit, pos_err, ci_P, pos_trials = process_unit(pos_final, T_BIN, n)
    neg_unit, neg_err, ci_N, neg_trials  = process_unit(neg_final, T_BIN, n)
    zero_unit, zero_err, ci_Z, zero_trials = process_unit(zero_final, T_BIN, n)

    ## store data as pkl
    f = open('neural.pos', 'wb')
    pickle.dump([pos_unit, pos_err, ci_P, pos_trials], f)
    f.close()

    f = open('neural.neg', 'wb')
    pickle.dump([neg_unit, neg_err, ci_N, neg_trials], f)
    f.close()

    f = open('neural.zero', 'wb')
    pickle.dump([zero_unit, zero_err, ci_Z, zero_trials], f)
    f.close()



