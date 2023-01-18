"""
SAVE_DATA is to obtain publication-ready plot and store data
author: naureen ghani

"""

import pickle
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from plot_utils import *
from scipy.ndimage import gaussian_filter
from mpl_toolkits.axes_grid1 import AxesGrid

def plot_unit(n, alignment_type, pos_color, neg_color, zero_color):

    f = open('neural.pos', 'rb')
    pos_unit, pos_err, ci_P, pos_trials = pickle.load(f)
    f.close()

    f = open('neural.neg', 'rb')
    neg_unit, neg_err, ci_N, neg_trials = pickle.load(f)
    f.close()

    f = open('neural.zero', 'rb')
    zero_unit, zero_err, ci_Z, zero_trials = pickle.load(f)
    f.close()

    times_sec = np.arange(-1,1,0.02)

    svfg = plt.figure(figsize=(10,8))
    figure_style()

    plt.plot(times_sec, gaussian_filter(pos_unit,sigma=3), lw=3, label=f"{pos_trials} pos trials", c=pos_color)
    plt.plot(times_sec, gaussian_filter(neg_unit,sigma=3), lw=3, label=f"{neg_trials} neg trials", c=neg_color)
    plt.plot(times_sec, gaussian_filter(zero_unit,sigma=3),lw=3, label=f"{zero_trials} zero trials", c=zero_color)

    ## sem error bars
    plt.fill_between(times_sec, gaussian_filter(pos_unit-pos_err, sigma=3), gaussian_filter(pos_unit+pos_err, sigma=3), alpha=0.2, color=pos_color)
    plt.fill_between(times_sec, gaussian_filter(neg_unit-neg_err, sigma=3), gaussian_filter(neg_unit+neg_err, sigma=3), alpha=0.2, color=neg_color)
    plt.fill_between(times_sec, gaussian_filter(zero_unit-zero_err, sigma=3), gaussian_filter(zero_unit+zero_err, sigma=3), alpha=0.2, color=zero_color)

    ## 95th percentile confidence intervals
    plt.plot(times_sec, gaussian_filter(pos_unit-ci_P, sigma=3), ls="--", c=pos_color)
    plt.plot(times_sec, gaussian_filter(pos_unit+ci_P, sigma=3), ls="--", c=pos_color)
    plt.plot(times_sec, gaussian_filter(neg_unit-ci_N, sigma=3), ls="--", c=neg_color)
    plt.plot(times_sec, gaussian_filter(neg_unit+ci_N, sigma=3), ls="--", c=neg_color)
    plt.plot(times_sec, gaussian_filter(zero_unit-ci_Z, sigma=3), ls="--", c=zero_color)
    plt.plot(times_sec, gaussian_filter(zero_unit+ci_Z, sigma=3), ls="--", c=zero_color)

    ## time 0
    plt.axvline(x=0, ls="--", c="k")

    ## labels
    plt.xlabel(f'time aligned to {alignment_type} [s]', fontsize=20)
    plt.ylabel('z-score firing rate', fontsize=20)
    plt.legend(fontsize=20, loc="upper left")
    plt.show()
    sns.despine(trim=True, offset=4)
    svfg.savefig(f"unit_{n}.png")

    print(f"saved plot for unit #{n}")

def plot_psth(reg, side):
    f = open('neural.data', 'rb')
    st_mat, fs_mat, ze_mat = pickle.load(f)
    f.close()

    fig, axes = plt.subplots(nrows=1, ncols=3)
    plt.subplot(1,3,1); plt.imshow(st_mat, cmap="bwr"); plt.clim([-3,3]); plt.axvline(x=50, c="k", ls="--"); psth_style()
    plt.title("stimulus-triggered", fontsize=10, fontweight="bold")
    plt.subplot(1,3,2); plt.imshow(fs_mat, cmap="bwr"); plt.clim([-3,3]); plt.axvline(x=50, c="k", ls="--"); psth_style()
    plt.title("false-starts", fontsize=10, fontweight="bold")
    plt.subplot(1,3,3); plt.imshow(ze_mat, cmap="bwr"); plt.clim([-3,3]); plt.axvline(x=50, c="k", ls="--"); psth_style()
    plt.title("zero-contrast", fontsize=10, fontweight="bold")

    #fig.subplots_adjust(right=0.8)
    #cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    #im = plt.imshow(np.random.random((10,10)), vmin=0, vmax=1, cmap="bwr")
    #cbar = fig.colorbar(im, cax=cbar_ax, ticks=[0, 0.5, 1])
    #cbar.ax.set_yticklabels(['-3', "0", '+3']) 
    #cbar.set_label('z-score firing rate', rotation=90, fontsize=8)

    fig.savefig(f"psth_{reg}_{side}.png", bbox_inches="tight", dpi=300)

    print("saved psth")

