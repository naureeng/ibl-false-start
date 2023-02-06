"""
BUILD_SAT creates speed-accuracy curves (by blocks)
note: sums cumulative choices across eids, plots error bars across eids
author: naureen ghani

"""
import sys
import random
import numpy as np
import matplotlib.pyplot as plt
sys.path.append('/nfs/nhome/live/naureeng/int-brain-lab/ibl-false-start/ephys')
from RT_dist_plot import *
from reaction_time_functions import *
from itertools import chain
import seaborn as sns
import pandas as pd
from process_behav import running_avg
from one.api import ONE

one = ONE(mode="local")
subject_name = "CSH_ZAD_026"

eids = one.search(subject=subject_name)

session = []; contrast = []; block = []; RT = []; outcome = []
for n in range(len(eids)):
    eid = eids[n]
    print(eid)
    try:
        trials = TrialData(eid)
    except:
        continue
    wheel = WheelData(eid)
    goCueRTs, stimOnRTs, durations, _ = compute_RTs(eid)
    n_trials = trials.total_trial_count
    print(n_trials, "trials")

    for i in range(n_trials):
        session.append(eid)
        contrast.append(trials.contrast[i])
        block.append(trials.probabilityLeft[i])
        RT.append(np.nan_to_num(goCueRTs[i]))
        outcome.append(trials.feedbackType[i])

concat_data = zip(session, contrast, block, RT, outcome)
df = pd.DataFrame(data=concat_data, columns=["eid", "contrast", "block", "RT", "outcome"])

## save data 
df.to_csv(f"{subject_name}.csv")
print("dataframe saved to csv")

## process the data
contrastTypes = [-1, -0.25, -0.125, -0.0625, 0, 0.0625, 0.125, 0.25, 1]
df = pd.read_csv(f'{subject_name}.csv', sep=',')
kde_plot(df, contrastTypes, "RT", "contrast", save_file=True)
print("saved plot")

cdf_data = cdf(df, conditions=contrastTypes)
cdf_plot(cdf_data, legend=False, save_file=True)

"""
## conditional accuracy functions [caf]
a = calc_caf(df[(df.contrast == "1")], "eid", "RT", "outcome", "1")
print(a)
"""

#data[contrast] = RTs_contrast

#svfg = plt.figure(figsize=(10,8))
#sns.stripplot(data, orient="h", jitter=True)
#plt.xlim([-0.2, 1])
#svfg.savefig("test.png")
