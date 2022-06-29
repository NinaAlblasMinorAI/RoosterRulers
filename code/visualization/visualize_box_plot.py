"""
- Programmeertheorie
- RoosterRulers - Lectures & Lesroosters

This file contains a function to visualize the box plots of malus points
of both the hillclimber and simulated annealing algorithm.
"""


from statistics import mean
import platform
from datetime import datetime

if platform.system() == "Darwin":
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib import pyplot as plt
else:
    import matplotlib.pyplot as plt


def visualize_box_plot(list_of_scores_hc, list_of_scores_sa):
    """
    Visualizes the malus points of both hillclimber and simulated annealing 
    into a single box plot.
    """

    # retrieve string of current date
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M")

    # store the scores in a dictionary
    scores = {
                "Hillclimber": list_of_scores_hc, 
                "Simulated Annealing": list_of_scores_sa
            }

    # get average and minimum hillclimber score
    average_hc = mean(list_of_scores_hc)
    minimum_hc = min(list_of_scores_hc)

    # get average and minimum simulated annealing score
    average_sa = mean(list_of_scores_sa)
    minimum_sa = min(list_of_scores_sa)

    # create the figure and its subplots
    fig, ax = plt.subplots(figsize=(6, 8))

    # create boxplot for both algorithms
    ax.boxplot(scores.values())

    # plot layout
    ax.set_xticklabels([f"$\\bfHillclimber$\nAverage: {round(average_hc)}\nMinimum: {minimum_hc}",
                        f"$\\bfSimulatedAnnealing$\nAverage: {round(average_sa)}\nMinimum: {minimum_sa}"])
    ax.set_title(f"Objective value of the valid solutions\nof the hillclimber and simulated annealing algorithms", fontweight="bold")

    # save figure
    plt.savefig(f"output_data/{dt_string}_boxplot.png", dpi=300)