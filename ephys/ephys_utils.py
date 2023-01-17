"""
EPHYS_UTILS is dependency functions for ephys data analysis
author: naureen ghani

"""

import numpy as np
import logging
import math
from brainbox.io.one import SpikeSortingLoader, load_channel_locations
from brainbox.processing import bincount2D
from one.api import ONE, alfio
one = ONE(mode="local")

def find_nearest(array, value):
    """
    FIND_NEAREST obtains the index where a value occurs in array
    author: michael schartner

    :param array: matrix [np.array]
    :param value: search input [int]
    :return idx: index in array where value occurs [int]

    """
    idx = np.searchsorted( array, value, side="left" )
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx]) ):
        return idx - 1
    else:
        return idx

def pair_firing_rate_contrast(eid, probe, d, reg, time_lower, time_upper, T_BIN, alignment_type):
    """
    PAIR_FIRING_RATE_CONTRAST obtains the spike data for a session
    :param eid: session [string]
    :param probe: probe [string]
    :param d: trials to index [dictionary]
    :param time_lower: time prior motionOnset in [sec] [int]
    :param time_upper: time post motionOnset in [sec] [int]
    :param T_BIN: bin size [sec] [int]
    :param alignment_type: "motionOnset" or "stimOnset" [string]
    :return Res: 3D matrix of spike data [trials x time x units] [np.array]
    :return num_units: num of units [int]
    :return histology: ids of Res in histology [pd.dataframe]
    """

    d_types = [f"alf/{probe}/spikes.times.npy", f"alf/{probe}/spikes.depths.npy", f"alf/{probe}/spikes.clusters.npy", f"alf/{probe}/clusters.channels.npy"] #, "alf/_ibl_trials.intervals.npy"]
    D = one.load_datasets(eid, datasets=d_types)
    print('data acquired')

    local_path = one.eid2path( eid )
    alf_path = local_path / 'alf'
    probe_path = alf_path / probe

    spikes = alfio.load_object( probe_path, 'spikes' )

    R, times, Clusters = bincount2D( spikes['times'], spikes['clusters'], T_BIN ) # raw spikes

    els = load_channel_locations( eid, one=one )

    Acronyms = els[probe]['acronym']
    clusters = alfio.load_object( probe_path, 'clusters' )
    cluster_chans = clusters['channels'][Clusters]
    acronyms = Acronyms[cluster_chans]

    ind_reg = [idx for idx, s in enumerate(acronyms) if reg in s]
    mask = np.zeros( len(acronyms), dtype='bool' )
    for i in ind_reg:
        mask[i] = 1

    D = R.T # transpose data

    Res = []

    # obtain mean firing rate and contrast
    m_ask = mask
    num_units = np.squeeze(np.where( m_ask==True ))
    noisy_units = 0

    if len(num_units) < 10: # min req of 10 neurons
        logging.error('not enough units')
    else:
        histology = [acronyms[i] for i in num_units]
        n_units = len(num_units)

    for i in d:
        if alignment_type == "motionOnset":
            start_idx = find_nearest(times, d[i][0])
            end_idx = find_nearest(times, d[i][1])
        else:
            start_idx = find_nearest(times, d[i][5])
            end_idx = find_nearest(times, d[i][6])

        data =  D[start_idx : end_idx, m_ask]
        data_len = (abs(time_lower) + abs(time_upper)) / T_BIN
        if len(data) != data_len:
            if len(data) < data_len:
                n = int(data_len - len(data))
                r, c = data.shape
                position_pad = np.zeros((n,c))
                data_final = np.append(data, position_pad, axis=0)
            else:
                logging.warning('data long')
                data_final = data[0: int(data_len) ]
        else:
            data_final = data

        Res.append(data_final)

    ## sanity check:
    n_trials = len(d)
    n_bins = int( (time_upper - time_lower) / T_BIN )

    ## [neurons x time x trials]
    Res = np.reshape(np.transpose(Res), [n_units, n_bins, n_trials])
    print(f"{n_units} units, {n_bins} bins, {n_trials} trials")

    ## mean firing rate over trials per unit
    mean_firing_unit = [(np.mean(np.mean(Res[i,:,:])) / T_BIN) for i in range(n_units)]
    noisy_value = [i for i in mean_firing_unit if i<=0.1 or i>=100]
    noisy_idx = []
    for i in range(n_units):
        print(f"unit:#{i}, mean:{mean_firing_unit[i]}")
        if mean_firing_unit[i]<=0.1 or mean_firing_unit[i]>=100:
            print("noisy unit")
            noisy_idx.append(i)
        else:
            print("good unit")
    
    print(len(noisy_idx), "noisy units")

    return Res, noisy_idx

def remove_noisy_units(pos_data, noisy_pos, neg_data, noisy_neg):
    if len(noisy_pos) != 0 or len(noisy_neg) != 0:
        noisy_idx = np.concatenate((noisy_pos, noisy_neg), axis=0)
        noisy_units = [int(x) for x in np.unique(noisy_idx)]
        pos_final = np.delete(pos_data, noisy_units, axis=0)
        neg_final = np.delete(neg_data, noisy_units, axis=0)
    else:
        pos_final = pos_data
        neg_final = neg_data

    return pos_final, neg_final
