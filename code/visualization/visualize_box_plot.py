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







    # fig = plt.figure(figsize=(10, 8))
    # gs = gridspec.GridSpec(nrows=1, ncols=2)#, width_ratios=[1,1], wspace=0.5)

    # # hillclimber
    # average_hc = mean(list_of_scores_hc)
    # minimum_hc = min(list_of_scores_hc)
    # maximum_hc = max(list_of_scores_hc)
    
    # ax1 = fig.add_subplot(gs[0])
    # ax1.boxplot(list_of_scores_hc)
    # ax1.tick_params(axis='y')#, labelcolor=color)
    # ax1.set_title(f"Objective value of the valid solutions\nof the hillclimber algorithm\n(N = {N})")
    # ax1.set_xticks([])
    # ax1.set_xlabel(f"Average: {round(average_hc)}\nMinimum: {minimum_hc}")
    # ax1.set_ylabel("Objective value")

    # # simulated annealing
    # average_sa = mean(list_of_scores_sa)
    # minimum_sa = min(list_of_scores_sa)
    # maximum_sa = max(list_of_scores_sa)

    # ax2 = fig.add_subplot(gs[1])
    # ax2.boxplot(list_of_scores_sa)
    # ax2.tick_params(axis='y')#, labelcolor=color)
    # ax2.set_title(f"Objective value of the valid solutions\nof the simulated annealing algorithm\n(N = {N})")
    # ax2.set_xticks([])
    # ax2.set_xlabel(f"Average: {round(average_sa)}\nMinimum: {minimum_sa}")
    # ax2.set_ylabel("Objective value")

    # y_min = min(minimum_hc, minimum_sa)
    # y_max = max(maximum_hc, maximum_sa)

    # ax1.set_ylim(y_min - 1, y_max + 1)
    # ax2.set_ylim(y_min - 1, y_max + 1)

    
    plt.savefig(f"output_data/{dt_string}_boxplot.png", dpi=300)