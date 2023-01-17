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

