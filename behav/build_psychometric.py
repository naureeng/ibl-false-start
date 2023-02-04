"""
BUILD_PSYCHOMETRIC creates psychometric function by blocks
note: sums cumulative choices across eids, plots error bars across eids
author: naureen ghani

"""

import numpy as np
import matplotlib.pyplot as plt
import pickle
from process_behav import *
from plot_behav import *

"""
## [1] load data
eids = np.load("eid-behav-qc.npy")
print(len(eids), "sessions")

## [2] process data
data = build_pyschometric_dict(eids, "posRT")
## store pickle
f = open('data.psycho', 'wb')
pickle.dump(data, f)
f.close()
print("data pickled")
"""

## [3] save data
f = open("posRT.psycho", "rb")
data = pickle.load(f)
plot_dict(data, "posRT")


