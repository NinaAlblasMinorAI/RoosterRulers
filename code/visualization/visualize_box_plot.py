from statistics import mean
import platform
from datetime import datetime

if platform.system() == "Darwin":
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib import pyplot as plt
else:
    import matplotlib.pyplot as plt


def visualize_box_plot(list_of_scores_hc, list_of_scores_sa, N, T, R1, R2, R3):
    """
    Visualizes a list of scores into a box plot.
    """

    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M")

    average_hc = mean(list_of_scores_hc)
    minimum_hc = min(list_of_scores_hc)

    average_sa = mean(list_of_scores_sa)
    minimum_sa = min(list_of_scores_sa)

    my_dict = {"Hillclimber": list_of_scores_hc, "Simulated Annealing": list_of_scores_sa}

    fig, ax = plt.subplots(figsize=(6, 8))
    ax.boxplot(my_dict.values())
    ax.set_xticklabels([f"$\\bfHillclimber$\nAverage: {round(average_hc)}\nMinimum: {minimum_hc}",
                        f"$\\bfSimulatedAnnealing$\nAverage: {round(average_sa)}\nMinimum: {minimum_sa}"])
    ax.set_title(f"Objective value of the valid solutions\nof the hillclimber and simulated annealing algorithms\n(T = {T}, $R_1$ = {R1}, $R_2$ = {R2}, $R_3$ = {R3}, N = {N})", fontweight="bold")

    
    plt.savefig(f"output_data/{dt_string}_boxplot.png", dpi=300)