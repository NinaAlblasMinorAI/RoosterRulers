from statistics import mean
import platform

if platform.system() == "Darwin":
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib import pyplot as plt
else:
    import matplotlib.pyplot as plt


def visualize_box_plot(list_of_scores, N):
    """
    Visualizes a list of scores into a box plot.
    """

    average = mean(list_of_scores)
    minimum = min(list_of_scores)


    plt.boxplot(list_of_scores)
    plt.title(f"Objective value of the valid solutions of the algorithm (N = {N})")
    plt.xticks([])
    plt.xlabel(f"Average: {round(average)}\nMinimum: {minimum}")
    plt.ylabel("Objective value")
    
    plt.savefig("output_data/boxplot.png")