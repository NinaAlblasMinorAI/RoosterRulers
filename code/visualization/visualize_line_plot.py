import platform
from datetime import datetime
if platform.system() == "Darwin":
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib import pyplot as plt
else:
    import matplotlib.pyplot as plt


def visualize_line_plot(list_of_points, algorithm):
    """
    Takes a list of malus points and visualizes them in a line plot
    against the number of iterations.
    """

    # retrieve string of current date
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M")

    # define number of iterations
    N = len(list_of_points)
    iterations = range(N)

    # create figure
    f = plt.figure()
    ax = f.add_subplot(111)

    # create line plot
    plt.plot(iterations, list_of_points)

    # add text to the upper right corner of plot to indicate minimum
    plt.text(x=0.8,
            y=0.9,
            s=f'minimum = {min(list_of_points)}', 
            color="red",
            horizontalalignment='center',
            verticalalignment='center', 
            transform = ax.transAxes)

    # create dotted line to indicate minimum
    plt.axhline(y = min(list_of_points), color = 'r', linestyle = ':')

    # plot layout
    plt.yscale("log")
    plt.xlabel("No. of mutations")
    plt.ylabel("Objective value")
    plt.subplots_adjust(top=0.85)
    plt.title(f"Objective value of the \n{algorithm} algorithm route", fontweight="bold")

    # save plot
    plt.savefig(f"output_data/{algorithm}_{dt_string}_plot.png", dpi=300)    