import numpy as np
import matplotlib.pyplot as plt
import pickle
import seaborn as sns
from plot_behav import figure_style
from scipy.stats import sem

f = open('falsestart.blockchange', 'rb')
[rightData, leftData] = pickle.load(f)

## plot data
right_data  = np.nanmean(rightData, axis=0)
left_data   = np.nanmean(leftData, axis=0) 
right_error = np.nanstd(rightData, axis=0)
left_error  = np.nanstd(leftData, axis=0)

T_BIN = 4
bins = np.arange(0,101,T_BIN)

svfg = plt.figure(figsize=(10,8))
figure_style()
plt.plot(bins, left_data, c="purple", lw=3, label="left block")
plt.scatter(bins, left_data, s=60, c="purple", lw=3)
plt.errorbar(bins, left_data, yerr=left_error, c="purple", lw=3)

plt.plot(bins, right_data, c="orange", lw=3, label="right block")
plt.scatter(bins, right_data, s=60, c="orange", lw=3)
plt.errorbar(bins, right_data, yerr=right_error, c="orange", lw=3)

plt.axhline(y=0.5, c="k", ls="--", lw=2)
plt.legend(loc="upper left", fontsize=20)

## 95% ci errorbars

plt.xlabel("#Trials since block change", fontsize=20)
plt.ylabel("Fraction of rightward movements", fontsize=20)
sns.despine(trim=True, offset=4)
svfg.savefig("false_start_block_switch.png")

