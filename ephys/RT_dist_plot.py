"""
reaction time analysis
return all significant wheel velocity changes in each trial
compute reaction times in relation to goCue and stimOn
author: naoki hiratani

"""

## import dependencies

import numpy as np
import scipy.stats as scist
import matplotlib.pyplot as plt
import sys

from math import *
from one.api import ONE, alfio
from os import path

one = ONE(mode="local")

contrastTypes = [0.0, 0.0625, 0.125, 0.25, 1.0]
ctlen = len(contrastTypes)

## pretty up plots
plt.rc('font',family='Arial')

class TrialData():
    def __init__(trials,eid):
        trial_data = one.load_object(eid, 'trials', collection='alf')
        trials.goCue_times = trial_data.goCue_times
        trials.stimOn_times = trial_data.stimOn_times
        trials.intervals = trial_data.intervals
        trials.feedback_times = trial_data.feedback_times
        trials.feedbackType = trial_data.feedbackType
        trials.contrastRight = trial_data.contrastRight
        trials.contrastLeft = trial_data.contrastLeft
        trials.choice = trial_data.choice
        trials.probabilityLeft = trial_data.probabilityLeft

        trials.total_trial_count = len(trials.goCue_times)

        ## supplementing the effective feedback time
        for tridx in range( len(trials.feedback_times) ):
            if isnan(trials.feedback_times[tridx]):
                trials.feedback_times[tridx] = trials.stimOn_times[tridx] + 60.0

    def psychometric_curve(trials, wheel_directions, reaction_times, false_start_threshold):
        total_trial_count = trials.total_trial_count
        trials.performance = np.zeros( (2,2,2*ctlen) ) ## early-late, left-right, contrast
        trials.fraction_choice_right = np.zeros( (2,2,2*ctlen) )
        trials.performance_cnts = np.zeros( (2,2,2*ctlen) )

        for tridx in range(total_trial_count):
            if trials.probLeft[tridx] != 0.5: ## within bias block only
                FStrial = 1 if reaction_times[tridx] < false_start_threshold else 0
                Rblock = 1 if trials.probLeft[tridx] < 0.5 else 0
                Rtrial = 1 if isnan(trials.contrastLeft[tridx]) else 0
                contrast_idx = 0
                for cidx in range(ctlen):
                    if Rtrial == 1:
                        if abs(trials.contrastRight[tridx] - contrastTypes[cidx]) < 0.001:
                            contrast_idx = ctlen + cidx
                    else:
                        if abs(trials.contrastLeft[tridx] - contrastTypes[cidx]) < 0.001:
                            contrast_idx = ctlen-1 - cidx
        ## wheel psychometric
        trials.fraction_choice_right[FStrial][Rblock][contrast_idx] += 0.5 + wheel_directions[tridx]/2.0
        trials.performance[FStrial][Rblock][contrast_idx] += 0.5 + 0.5*np.sign ( (Rtrial-0.5)*wheel_directions[tridx] )
        trials.performance_cnts[FStrial][Rblock][contrast_idx] += 1.0

class WheelData():
    def __init__(wheel, eid):
        wheel_data = one.load_object(eid, 'wheel', collection='alf')
        wheel.position = wheel_data.position
        wheel.timestamps = wheel_data.timestamps
        if str(type(wheel.position)) == "<class 'pathlib.PosixPath'>" or \
            str(type(wheel.timestamps)) == "<class 'pathlib.PosixPath'>":
            wheel.data_error = True
        else:
            wheel_velocity = []; wheel_velocity.append(0.0);
            for widx in range( len(wheel.position)-1 ):
                wheel_velocity.append( (wheel.position[widx+1] - wheel.position[widx])/(wheel.timestamps[widx+1] - wheel.timestamps[widx]) )
                wheel.velocity = wheel_velocity

    def calc_trialwise_wheel(wheel, stimOn_times, feedback_times):
        ## divide the wheel information into trialwise format
        ## stimOn_time - pre_duration < t < feedback_time

        wheel.stimOn_pre_duration = 0.3 # [s]
        wheel.total_trial_count = len(stimOn_times)

        wheel.trial_position = []
        wheel.trial_timestamps = []
        wheel.trial_velocity = []
        for tridx in range( wheel.total_trial_count ):
            wheel.trial_position.append([])
            wheel.trial_timestamps.append([])
            wheel.trial_velocity.append([])

        tridx = 0
        for tsidx in range( len(wheel.timestamps) ):
            timestamp = wheel.timestamps[tsidx]

            while tridx < len(stimOn_times) - 1 and timestamp > stimOn_times[tridx+1] - wheel.stimOn_pre_duration:
                tridx += 1
            if stimOn_times[tridx] - wheel.stimOn_pre_duration <= timestamp and timestamp < feedback_times[tridx]:
                wheel.trial_position[tridx].append( wheel.position[tsidx] )
                wheel.trial_timestamps[tridx].append( wheel.timestamps[tsidx] )
                wheel.trial_velocity[tridx].append( wheel.velocity[tsidx] )

    def calc_movement_onset_times(wheel, stimOn_times):
        ## a collection of timestamps with a significant speed (>0.5s) after more than 50ms

        speed_threshold = 0.5
        duration_threshold = 0.05 # [s]

        wheel.movement_onset_times = []
        wheel.first_movement_onset_times = np.zeros( (wheel.total_trial_count) ) 
        wheel.last_movement_onset_times = np.zeros( (wheel.total_trial_count) )
        wheel.movement_onset_counts = np.zeros( (wheel.total_trial_count) ) 
        
        wheel.movement_directions = []
        wheel.first_movement_directions = np.zeros( (wheel.total_trial_count) )
        wheel.last_movement_directions = np.zeros( (wheel.total_trial_count) )

        for tridx in range( len(wheel.trial_timestamps) ):
            wheel.movement_onset_times.append([])
            wheel.movement_directions.append([])
            cm_dur = 0.0; # continuous stationary duration
            for tpidx in range( len(wheel.trial_timestamps[tridx]) ):
                t = wheel.trial_timestamps[tridx][tpidx];
                if tpidx == 0:
                    tprev = stimOn_times[tridx] - wheel.stimOn_pre_duration
                cm_dur += (t - tprev)
                if abs(wheel.trial_velocity[tridx][tpidx]) > speed_threshold:
                    if cm_dur > duration_threshold: 
                        wheel.movement_onset_times[tridx].append( t )
                        wheel.movement_directions[tridx].append( np.sign(wheel.trial_velocity[tridx][tpidx]) )
                    cm_dur = 0.0;
                tprev = t
            wheel.movement_onset_counts[tridx] = len(wheel.movement_onset_times[tridx])
            if len(wheel.movement_onset_times[tridx]) == 0: # trials with no explicit movement
                wheel.first_movement_onset_times[tridx] = np.NaN
                wheel.last_movement_onset_times[tridx] = np.NaN
                wheel.first_movement_directions = 0
                wheel.last_movement_directions = 0
            else:
                wheel.first_movement_onset_times[tridx] = wheel.movement_onset_times[tridx][0]
                wheel.last_movement_onset_times[tridx] = wheel.movement_onset_times[tridx][-1]
                wheel.first_movement_directions[tridx] = wheel.movement_directions[tridx][0]
                wheel.last_movement_directions[tridx] = wheel.movement_directions[tridx][-1]

def compute_RTs(eid):
    goCueRTs = []; stimOnRTs = []
    trials = TrialData(eid)
    wheel = WheelData(eid)
    wheel.calc_trialwise_wheel(trials.stimOn_times, trials.feedback_times)
    wheel.calc_movement_onset_times(trials.stimOn_times)
    durations = trials.feedback_times - trials.stimOn_times 

    for rtidx in range( len(wheel.first_movement_onset_times) ):
        goCueRTs.append(wheel.first_movement_onset_times[rtidx] - trials.goCue_times[rtidx])
        stimOnRTs.append(wheel.first_movement_onset_times[rtidx] - trials.stimOn_times[rtidx])

    return goCueRTs, stimOnRTs, durations


