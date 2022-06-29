"""
- Programmeertheorie
- RoosterRulers - Lectures & Lesroosters

This file contains a function to visualize the box plots of malus points
of both the hillclimber and simulated annealing algorithm.
"""


from statistics import mean
import platform
from datetime import datetime
import numpy as np

if platform.system() == "Darwin":
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib import pyplot as plt
else:
    import matplotlib.pyplot as plt


def visualize_box_plot(list_of_points, algorithm, N=None, R1=None, R2=None, R3=None, T=None, O=1, c=10):
    """
    Visualizes the malus points of both hillclimber and simulated annealing 
    into a single box plot.
    """

    # # turn off warning that the two lists of scores aren't of equal length
    # np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)                 

    # retrieve string of current date
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M")

    # get average and minimum score
    average = mean(list_of_points)
    minimum = min(list_of_points)

    # create the boxplot
    plt.figure(figsize=(6, 8))
    plt.boxplot(list_of_points)

    # plot layout
    plt.xticks([])
    plt.xlabel(f"Average: {average}\nMinimum: {minimum}")
    plt.ylabel("Objective value")

    if algorithm == "hillclimber":
        plt.title("Objective value of the\nhillclimber algorithm route\n" +
                    f"($R_1$ = {R1}, $R_2$ = {R2}, $R_3$ = {R3}, {O} splits of {c} lessons, N = {N})", 
                    fontweight="bold")

    elif algorithm == "simulated_annealing":
        plt.title("Objective value of the\n" +
                    "simulated annealing algorithm route\n" +
                    f"(T = {T}, $R_1$ = {R1}, $R_2$ = {R2}, $R_3$ = {R3}, {O} splits of {c} lessons, N = {N})", 
                    fontweight="bold")

    # save figure
    plt.savefig(f"output_data/{algorithm}_{dt_string}_boxplot.png", dpi=300)