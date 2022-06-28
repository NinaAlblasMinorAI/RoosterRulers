import platform
from datetime import datetime
if platform.system() == "Darwin":
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib import pyplot as plt
else:
    import matplotlib.pyplot as plt


def visualize_line_plot(list_of_points, algorithm):

    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M")

    N = len(list_of_points)
    iterations = range(N)

    f = plt.figure()
    ax = f.add_subplot(111)

    plt.text(x=0.8,
            y=0.9,
            s=f'minimum = {min(list_of_points)}', 
            color="red",
            horizontalalignment='center',
            verticalalignment='center', 
            transform = ax.transAxes)

    plt.plot(iterations, list_of_points)
    plt.axhline(y = min(list_of_points), color = 'r', linestyle = ':')
    plt.yscale("log")
    plt.xlabel("No. of mutations")
    plt.ylabel("Objective value")
    plt.subplots_adjust(top=0.85)
    plt.title(f"Objective value of the \n{algorithm} algorithm route", fontweight="bold")

    plt.savefig(f"output_data/{algorithm}_{dt_string}_plot.png", dpi=300)    