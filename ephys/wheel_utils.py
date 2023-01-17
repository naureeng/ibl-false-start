"""
WHEEL_UTILS is dependency functions for wheel data analysis
author: naureen ghani

"""
from RT_dist_plot import *

def get_extended_trial_windows(eid, negRT_low, posRT_low, posRT_up, time_lower, time_upper, duration_threshold, movement_type):
    """
    GET_EXTENDED_TRIAL_WINDOWS creates dictionaries for ballistic and total movements 
    :param eid: session [string]
    :param negRT_low: lower bound for negRT [sec] [int]
    :param posRT_low: lower bound for posRT [sec] [int]
    :param posRT_up: upperbound for posRT [sec] [int]
    :param time_lower: time prior motionOnset in [sec] [int]
    :param time_upper: time post motionOnset in [sec] [int]
    :param duration_threshold: maximum trial duration [sec] [int]
    :param movement_type: "ballistic" or "total" 
    :return d_left_total, d_neg_left_total, d_right_total, d_neg_right_total, d_left, d_neg_left, d_right, d_neg_right
    posRT [L], negRT [L], posRT [R], negRT [R] for total and ballistic wheel movements   
    :return trial_time_all: total time data [sec]
    :return trial_position_all: total position data [degrees]
    :return trial_velocity_all: total velocity data [degrees/sec]
    """

    trials = TrialData(eid)
    wheel = WheelData(eid)
    wheel.calc_trialwise_wheel(trials.stimOn_times, trials.feedback_times)
    wheel.calc_movement_onset_times(trials.stimOn_times)

    ## compute contrast for trialData 
    trials.contrast = np.empty(trials.total_trial_count)
    contrastRight_idx = np.where(~np.isnan(trials.contrastRight))[0]
    contrastLeft_idx = np.where(~np.isnan(trials.contrastLeft))[0]

    trials.contrast[contrastRight_idx] = trials.contrastRight[contrastRight_idx]
    trials.contrast[contrastLeft_idx] = -1 * trials.contrastLeft[contrastLeft_idx]

    ## compute RTs
    goCueRTs, stimOnRTs, durations = compute_RTs(eid)

    ## wheel data
    trial_time_all = wheel.trial_timestamps
    trial_position_all = wheel.trial_position
    trial_velocity_all = wheel.trial_velocity

    ## build dicts
    d_left = {}; d_right = {}; d_neg_left = {}; d_neg_right = {}; d_zero_left = {}; d_zero_right = {} 

    for tr in range(trials.total_trial_count):
        a = wheel.first_movement_onset_times[tr]
        b = trials.goCue_times[tr]
        c = trials.feedback_times[tr]
        e = trials.contrast[tr]
        f = trials.choice[tr]
        g = trials.stimOn_times[tr]
        h = trials.probabilityLeft[tr]
        i = wheel.trial_position[tr] - wheel.trial_position[tr][0]
        j = wheel.trial_velocity[tr] - wheel.trial_velocity[tr][0]
        k = wheel.first_movement_directions[tr]
        m = trials.feedbackType[tr]
        neg_data = len( np.argwhere(i < 0) )
        pos_data = len( np.argwhere(i > 0) )
        neg_data_v = len( np.argwhere( j < 0 ))
        pos_data_v = len( np.argwhere( j > 0 ))
        movement_onsets = wheel.movement_onset_counts[tr]

        if np.isnan(c): # exclude trials with nan entries
            #print(f'feedback time is nan for trial {tr} and eid {eid}')
            continue

        if np.isnan(b): # exclude trials with nan entries
            continue
        
        if abs(g - b) >= 0.03: # exclude trials with non-synchronous goCue and stimOn times
            continue
            
        react = np.round(a - b, 3)

        if movement_type == "ballistic":
            ## ballistic wheel movements 
            if (react < negRT_low) and (c-b <= duration_threshold) and (movement_onsets==1) and (k==1) and (f==-1) and (neg_data_v<10):
                d_neg_left[tr] = [a+time_lower, a+time_upper, a, react, e, g+time_lower, g+time_upper, m, g]
                continue

            if (react < negRT_low) and (c-b <= duration_threshold) and (movement_onsets==1) and (k==-1) and (f==1) and (pos_data_v<10):
                d_neg_right[tr] = [a+time_lower, a+time_upper, a, react, e, g+time_lower, g+time_upper, m, g]
                continue

            if (react > posRT_low) and (react < posRT_up) and (c-b <= duration_threshold) and (movement_onsets==1) and (k==1) and (f==-1) and (neg_data_v<10):
                d_left[tr] = [a+time_lower, a+time_upper, a, react, e, g+time_lower, g+time_upper, m, g]
                continue

            if (react > posRT_low) and (react < posRT_up) and (c-b <= duration_threshold) and (movement_onsets==1) and (k==-1) and (f==1) and (pos_data_v<10): 
                d_right[tr] = [a+time_lower, a+time_upper, a, react, e, g+time_lower, g+time_upper, m, g]
                continue

            if (e==0) and (k==1) and (f==-1) and (neg_data_v<10):
                d_zero_left[tr] = [a+time_lower, a+time_upper, a, react, e, g+time_lower, g+time_upper, m, g]
                continue

            if (e==0) and (k==-1) and (f==1) and (pos_data_v<10):
                d_zero_right[tr] = [a+time_lower, a+time_upper, a, react, e, g+time_lower, g+time_upper, m, g]
                continue

        else:
            ## total wheel movements
            if (react > posRT_low) and (react < posRT_up) and (k==1):
                d_left[tr] = [a+time_lower, a+time_upper, a, react, e, g+time_lower, g+time_upper, m, g]
                continue

            if (react > posRT_low) and (react < posRT_up) and (k==-1):
                d_right[tr] = [a+time_lower, a+time_upper, a, react, e, g+time_lower, g+time_upper, m, g]
                continue

            if (react < negRT_low) and (k==1):
                d_neg_left[tr] = [a+time_lower, a+time_upper, a, react, e, g+time_lower, g+time_upper, m, g]
                continue

            if (react < negRT_low) and (k==-1):
                d_neg_right[tr] = [a+time_lower, a+time_upper, a, react, e, g+time_lower, g+time_upper, m, g]
                continue

            if (e==0) and (k==1):
                d_zero_left[tr] = [a+time_lower, a+time_upper, a, react, e, g+time_lower, g+time_upper, m, g]
                continue

            if (e==0) and (k==-1):
                d_zero_right[tr] = [a+time_lower, a+time_upper, a, react, e, g+time_lower, g+time_upper, m, g]

    return d_left, d_neg_left, d_right, d_neg_right, d_zero_left, d_zero_right, trial_time_all, trial_position_all, trial_velocity_all 
