import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from plot_behav import figure_style
from process_behav import compute_N_mice

df = pd.read_csv("cost_benefit_analysis.csv")
n_mice, _, _ = compute_N_mice(np.load("eid_behav_qc.npy"))

fig, ax = plt.subplots()
ax.scatter(df["t_loss"], df["t_gain"], c="k", s=1, zorder=10)
n_sessions = len(df["t_loss"])

lims = [
    np.min([ax.get_xlim(), ax.get_ylim()]),  # min of both axes
    np.max([ax.get_xlim(), ax.get_ylim()]),  # max of both axes
]

# now plot both limits against each other
ax.plot(lims, lims, 'k-', alpha=0.75, zorder=2)
ax.set_aspect('equal')
ax.set_xlim(lims)
ax.set_ylim(lims)
plt.xlim([-1,2])
plt.ylim([-1,2])
plt.axvline(x=-0.78, c="k", ls="--", lw=1)
plt.axhline(y=0.28, c="k", ls="--", lw=1)
plt.axhline(y=0, c="k", ls="--", lw=1)

plt.xlabel("avg time loss per trial [sec]")
plt.ylabel("avg time gain per trial [sec]")
plt.title(f"n = {n_sessions} sessions for {n_mice} mice")
sns.despine(trim=True, offset=4)
fig.savefig("cost_benefit.png", dpi=300)


