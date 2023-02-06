"""
dependency functions for reaction time analysis
author: erik marsja

"""

from __future__ import division
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def kde_plot(df, conditions, dv, col_name, save_file=False):
    sns.set_style("white")
    sns.set_style("ticks")
    diverging_colors = sns.color_palette("PiYG", 9)
    sns.set_palette(diverging_colors)
    svfg = plt.figure(figsize=(10,8))
    plt.rcParams['font.sans-serif'] = "Arial"
    plt.rcParams['font.family'] = "sans-serif"
    plt.rcParams['xtick.labelsize'] = 20
    plt.rcParams['ytick.labelsize'] = 20
    plt.rcParams["axes.linewidth"] = 2

    for condition in conditions:
        condition_data = df[(df[col_name] == condition)][dv]
        sns.kdeplot(condition_data, label=condition, lw=3)
        
    plt.legend(fontsize=20, loc="upper right") 
    plt.axvline(x=0.08, c="k", lw=3, ls="--")
    plt.xlim([-4,4])
    plt.xlabel("reaction time [movementOnset - stimulusOnset] (sec)", fontsize=20)
    plt.ylabel("counts", fontsize=20)
    sns.despine(trim=True, offset=4)

    if save_file:
        svfg.savefig("kde_seaborn_python_reaction_time.png")

def cdf(df, conditions=["-1", "-0.25", "-0.125", "-0.0625", "0", "0.0625", "0.125", "0.25", "1"]):
    data = {i: df[(df.contrast==conditions[i])] for i in range(len(conditions))}

    plot_data = []
    for i, condition in enumerate(conditions):
        rt = data[i].RT.sort_values()
        yvals = np.arange(len(rt)) / float(len(rt))

        ## append to data
        cond = [condition]*len(yvals)

        df = pd.DataFrame(dict(dens=yvals, dv=rt, condition=cond))
        plot_data.append(df)

    plot_data = pd.concat(plot_data, axis=0)

    return plot_data

def cdf_plot(cdf_data, save_file=False, legend=True):
    sns.set_style("white")
    sns.set_style("ticks")
    diverging_colors = sns.color_palette("PiYG", 9)
    sns.set_palette(diverging_colors)

    plt.rcParams['font.sans-serif'] = "Arial"
    plt.rcParams['font.family'] = "sans-serif"
    plt.rcParams['xtick.labelsize'] = 20
    plt.rcParams['ytick.labelsize'] = 20
    plt.rcParams["axes.linewidth"] = 2

    g = sns.FacetGrid(cdf_data, hue="condition", height=8, aspect=1, legend_out=False)
    g.map(plt.plot, "dv", "dens", lw=3)
    if legend:
        g.add_legend(fontsize=20, loc="lower right")
    g.set_axis_labels("reaction time [movementOnset - stimulusOnset] (sec)", "probability", fontsize=20)

    plt.xlim([0,8])
    sns.despine(trim=True,offset=4)

    if save_file:
        g.savefig("cumulative_density_functions_seaborn_python_reaction_time.png")

    plt.show()

def calc_caf(df, subid, rt, acc, trialtype, quantiles=[0.25, 0.50, 0.75, 1]):

    # subjects
    subjects = pd.Series(df[subid].values.ravel()).unique().tolist()
    subjects.sort()

    # multi-index frame for data
    arrays = [np.array(["rt"] * len(quantiles) + ["acc"] * len(quantiles)), np.array(quantiles *2)]
    data_caf = pd.DataFrame(columns=subjects, index=arrays)

    # calculate CAF (conditional accuracy function) for each subject
    for subject in subjects:

        sub_data = df.loc[(df[subid] == subject)]
        subject_df = sub_data[rt].quantile(q=quantiles).values

        # calculate mean reaction time and proportion of error for each bin
        for i, q in enumerate(subject_cdf):
            
            quantile = quantiles[i]

            # first
            if i < 1:
                # subset
                temp_df = sub_data[(sub_data[rt] < subject_cdf[i])]
                # RT
                data_caf.loc[("rt", quantile)][subject] = temp_df[rt].mean()
                # accuracy
                data_caf.loc[("acc", quantile)][subject] = temp_df[acc].mean()

            elif i == 1 or i < len(quantiles):
                # subset
                temp_df = sub_data[(sub_data[rt] > subject_cdf[i])]
                # RT
                data_caf.loc[("rt", quantile)][subject] = temp_df[rt].mean()
                # accuracy
                data_caf.loc[("acc", quantile)][subject] = temp_df[acc].mean()

            # last

            elif i == len(quantiles):
                # subset
                temp_df = sub_data[(sub_data[rt] > subject_cdf[i])]
                # RT
                data_caf.loc[("rt", quantile)][subject] = temp_df[rt].mean()
                # accuracy
                data_caf.loc[("acc", quantile)][subject] = temp_df[acc].mean()

        # aggregate subjects CAFs
        data_caf = data_caf.mean(axis=1).unstack(level=0)

        # add trialtype
        data_caf["contrast"] = [condition for _ in range(len(quantiles))]

        return data_caf


