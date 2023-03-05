"""
cost-benefit analysis for false start
author: naureen ghani

"""
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pickle
sys.path.append('/nfs/nhome/live/naureeng/int-brain-lab/ibl-false-start/ephys')
from RT_dist_plot import *
from one.api import ONE
from ibllib.io.extractors.training_trials import PhasePosQuiescence
from ibllib.io.extractors.biased_trials import ProbaContrasts
from ibllib.io.extractors.base import get_session_extractor_type

one = ONE()

def compute_quiescence(eid):
    raw_task_data = one.list_datasets(eid, filename='_iblrig_task*', collection='raw_behavior_data')
    one.load_datasets(eid, raw_task_data, download_only=True)
    session_path = one.eid2path(eid)
    
    (*_, quiescence), _ = PhasePosQuiescence(session_path).extract(save=False)

    return list(quiescence)

eids = np.load("eid_behav_qc.npy")
print(len(eids), "sessions")

df = pd.DataFrame([], columns=["eid", "t_loss", "t_gain", "quiescence"])
for i in range(100):
    eid = eids[i]
    print(eid)
    try:
        trials = TrialData(eid)
        quiescence = compute_quiescence(eid)
        goCueRTs, stimOnRTs, duration, wheel = compute_RTs(eid)

    ## trials.intervals[n,0] = start of quiescent period
    ## trials.intervals[n,1] = stimulusOff

        quiescence_pd = [trials.stimOn_times[n]-trials.intervals[n,0] for n in range(len(trials.stimOn_times))]

        idx = [i for i in range(len(goCueRTs)) if goCueRTs[i]<=0.08 and goCueRTs[i]>=-0.20]

        negRT = [i for i in goCueRTs if i<=0.08 and i>=-0.20]
        t_gain = [0.08-i for i in goCueRTs if i<=0.08 and i>=-0.20]
        t_loss = [quiescence_pd[i] for i in idx]  
        quiescence = [quiescence[i] for i in idx]  

        df.loc[i, ["eid"]] = eid
        df.loc[i, ["t_loss"]] = np.nanmean(t_loss)
        df.loc[i, ["t_gain"]] = np.nanmean(t_gain)
        df.loc[i, ["quiescence"]] = np.nanmean(quiescence)
    except:
        continue

## save data
df.to_csv(f"cost_benefit_analysis.csv")
print("dataframe saved to csv")

