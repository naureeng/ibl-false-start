"""
MOUSE_WIDE is analysis of many expert mice
author: naureen ghani

"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sys
sys.path.append('/nfs/nhome/live/naureeng/int-brain-lab/ibl-false-start/ephys')
from plot_utils import *

df = pd.read_excel('expert_mouse.xlsx')
print(len(df), "expert mice")

prop_fs_mouse = []
rwd_rate_mouse = []
hit_rate_mouse = []
fs_mean_mouse = []
late_mean_mouse = []

svfg_one = plt.figure(figsize=(10,8))
for i in range(len(df)):
    subject_name = df["subject_name"][i]
    try:
        median_prop_fs = np.load(f"/nfs/gatsbystor/naureeng/expert_mouse/{subject_name}/median_prop_fs.npy")
        prop_fs_mouse.append(median_prop_fs)
        median_rwd_rate = np.load(f"/nfs/gatsbystor/naureeng/expert_mouse/{subject_name}/median_rwd_rate.npy")
        rwd_rate_mouse.append(median_rwd_rate)
        median_hit_rate = np.load(f"/nfs/gatsbystor/naureeng/expert_mouse/{subject_name}/median_hit_rate.npy")
        hit_rate_mouse.append(median_hit_rate)

        ##
        with np.load(f"/nfs/gatsbystor/naureeng/expert_mouse/{subject_name}/fs_mean.npz") as npz:
            fs_mean = np.ma.MaskedArray(**npz)
        fs_mean_mouse.append(fs_mean[0:800])
        
        with np.load(f"/nfs/gatsbystor/naureeng/expert_mouse/{subject_name}/late_mean.npz") as npz:
            late_mean = np.ma.MaskedArray(**npz)
        late_mean_mouse.append(late_mean[0:800])

    except:
        continue

fs_mean, fs_error = tolerant_mean(fs_mean_mouse)
late_mean, late_error = tolerant_mean(late_mean_mouse)
unit_time = np.linspace(0,1,len(fs_mean))
plt.plot(unit_time, fs_mean, lw=2, color="b", label="false starts")
plt.fill_between(unit_time, fs_mean-fs_error, fs_mean+fs_error, alpha=0.2, color="b")
plt.plot(unit_time, late_mean, lw=2, color="k", label="late trials")
plt.fill_between(unit_time, late_mean-late_error, late_mean+late_error, alpha=0.2, color="k")
plt.xlabel("relative position within a session", fontsize=20)
plt.ylabel("fraction of trials", fontsize=20)
plt.legend(fontsize=20)
plt.title(f"n = {len(prop_fs_mouse)} expert mice", fontsize=20, fontweight="bold")
figure_style()
sns.despine(trim=True, offset=4)

svfg_one.savefig("running_position.png")

"""
svfg = plt.figure(figsize=(10,8))
figure_style()
plt.scatter(prop_fs_mouse, hit_rate_mouse, s=100, cmap="jet")
cbar = plt.colorbar()
cbar.set_label('hit rate [%]', fontsize=20)
y = rwd_rate_mouse
x = prop_fs_mouse
a, b = np.polyfit(x, y, 1)
#plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)), c="k", lw=2, label=f"y={round(a,3)}*x+{round(b,3)}")
plt.legend(fontsize=20)
plt.ylabel("reward rate [uL/sec]", fontsize=20)
plt.xlabel("fraction of false starts", fontsize=20)
plt.title(f"n = {len(x)} expert mice", fontsize=20, fontweight="bold")
sns.despine(trim=True, offset=4)
svfg.savefig("rwd_rate_mouse.png")
"""


