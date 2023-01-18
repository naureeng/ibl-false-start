"""
PLOT_UTILS is dependency functions for plotting
author: naureen ghani

"""
import matplotlib.pyplot as plt

def figure_style():
    ## parameters in plot-style
    plt.rcParams['font.sans-serif'] = "Arial"
    plt.rcParams['font.family'] = "sans-serif"
    plt.rcParams['xtick.labelsize'] = 20
    plt.rcParams['ytick.labelsize'] = 20
    plt.rcParams["axes.linewidth"] = 2

def psth_style():
    x = [0,50,100]
    labels = ['-1','0',1]
    plt.xticks(x, labels, fontsize=8)
    plt.xlabel("time to motionOnset [sec]", fontsize=8)
    plt.ylabel("#units", fontsize=8)
    plt.tight_layout()
