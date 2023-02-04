"""
PLOT_BEHAV is to plot behavioral data
author: naureen ghani

"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from statsmodels.formula.api import ols
import statsmodels.api as sm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from process_behav import *
sys.path.append('/nfs/nhome/live/naureeng/int-brain-lab/ibl-false-start/ephys')
from plot_utils import *
import seaborn as sns

## plot time in session vs frac of trials
def plot_session_position(subject_name, RTs, i, window):
    svfg = plt.figure(figsize=(10,8))
    fs_rate, late_rate = fs_analysis(RTs, i, window)
    # fs-trials
    plt.plot(fs_rate, label="false starts")
    # late-trials
    plt.plot(late_rate, label="late trials")
    # labe
    plt.xlabel("relative position within a session", fontsize=12)
    plt.ylabel("fraction of trials", fontsize=12)
    plt.legend(fontsize=12)
    svfg.savefig(f"/nfs/gatsbystor/naureeng/expert_mouse/{subject_name}/{subject_name}_session_position.png")

def plot_mouse_position(subject_name, fs_eids, late_eids, n_eids):
    svfg = plt.figure(figsize=(10,8))
    figure_style()
    #[plt.plot(fs_eids[i], c="b", lw=0.5) for i in range(len(fs_eids))]
    #[plt.plot(late_eids[i], c="k", lw=0.5) for i in range(len(late_eids))]
    fs_mean, fs_error = tolerant_mean(fs_eids)
    late_mean, late_error = tolerant_mean(late_eids)
    
    unit_time = np.linspace(0,1,len(fs_mean))
    plt.plot(unit_time, fs_mean, lw=2, color="b", label="false starts")
    plt.fill_between(unit_time, fs_mean-fs_error, fs_mean+fs_error, alpha=0.2, color="b")
    plt.plot(unit_time, late_mean, lw=2, color="k", label="late trials")
    plt.fill_between(unit_time, late_mean-late_error, late_mean+late_error, alpha=0.2, color="k")
    plt.xlabel("relative position within a session", fontsize=20)
    plt.ylabel("fraction of trials", fontsize=20)
    plt.legend(fontsize=20)
    sns.despine(trim=True, offset=4) 
    svfg.savefig(f"/nfs/gatsbystor/naureeng/expert_mouse/{subject_name}/{subject_name}_mouse_position.png")

    return fs_mean, fs_error, late_mean, late_error

def plot_mouse_rate(subject_name, total_rwd, prop_fs, hit_rate):
    svfg = plt.figure(figsize=(10,8))
    plt.scatter(total_rwd, prop_fs, c=hit_rate, s=100)
    plt.xlabel("reward rate [uL/sec]", fontsize=20)
    plt.ylabel("fraction of false starts", fontsize=20)
    cbar = plt.colorbar()
    cbar.set_label('hit rate [%]', fontsize=20)
    sns.despine(trim=True, offset=4)
    svfg.savefig(f"/nfs/gatsbystor/naureeng/expert_mouse/{subject_name}/{subject_name}_mouse_rwd_rate.png")

def plot_data(xdata, data_fracR, data_total, ldata, cdata):

    data_block = sum(data_fracR) / sum(data_total)
    data_eid = [i / (j+0.0001) for i, j in zip(data_fracR, data_total)]
    print(len(data_eid))
    std_block = np.std(data_eid, axis=0)
    sem_block = stats.sem(data_eid, axis=0)
    ci_95 = 1.96*sem_block

    plt.plot(xdata, data_block, lw=3, label=ldata, color=cdata)
    plt.scatter(xdata, data_block, 100, c=cdata)

    ## 95 % confidence intervals
    plt.errorbar(xdata, data_block, yerr=ci_95*10, fmt="o", c=cdata, elinewidth=3 )

    return list(data_block)


def plot_dict(data, name):
    svfg = plt.figure(figsize=(10,8))
    plt.rcParams['font.sans-serif'] = "Arial"
    plt.rcParams['font.family'] = "sans-serif"
    plt.rcParams['xtick.labelsize'] = 20
    plt.rcParams['ytick.labelsize'] = 20
    plt.rcParams["axes.linewidth"] = 2

    ## [2] process data
    contrastTypes = [-1.0, -0.25, -0.125, -0.0625, -0.0, 0.0, 0.0625, 0.125, 0.25, 1.0]

    data_80 = plot_data(contrastTypes, data["80_fracR"], data["80_total"], "left block", "#3e2f5b" )
    data_20 = plot_data(contrastTypes, data["20_fracR"], data["20_total"], "right block", "#f28500" )
    data_50 = plot_data(contrastTypes, data["50_fracR"], data["50_total"], "unbiased block", "dimgrey" )

    ## [3] statistical analysis
    x = np.concatenate( (data_80,data_20,data_50), axis=0)
    df = pd.DataFrame({'fracR': x, 'block': np.repeat(['80', '20', '50'], repeats=10), 'contrast': np.tile(contrastTypes, reps=3)})
    model = ols('fracR ~ C(contrast) + C(block) + C(contrast):C(block)', data=df).fit()
    print(sm.stats.anova_lm(model, typ=2))
    tukey = pairwise_tukeyhsd(endog=df['fracR'], groups=df['block'], alpha=0.05)
    print(tukey)

    ## plot labels
    sns.despine(trim=True, offset=4)
    plt.xlabel('Contrast (%)', fontsize=20)
    plt.ylabel('Fraction of rightward choices', fontsize=20)
    plt.legend(loc="upper left", fontsize=20)
    plt.xticks([-1, -0.125, 0, 0, 0.125, 1], ["-100", "-12.5", "0.0", "0.0","12.5", "100"], rotation=45)
    plt.yticks(np.arange(0,1.2,step=0.2))
    plt.ylim([-0.2,1.2])
    plt.tight_layout()

    ## save plot
    svfg.savefig(f"false_start_frac_right_{name}.png")

