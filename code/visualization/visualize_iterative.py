import platform
from datetime import datetime
if platform.system() == "Darwin":
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib import pyplot as plt
else:
    import matplotlib.pyplot as plt


def visualize_iterative(list_of_points, algorithm):

    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M")

    plt.figure()

    N = len(list_of_points)
    
    iterations = range(N)
    malus_points = list_of_points
    
    plt.plot(iterations, malus_points)
    plt.axhline(y = 0, color = 'r', linestyle = ':')
    plt.yscale("log")
    plt.xlabel("No. of iterations")
    plt.ylabel("Objective value")
    plt.subplots_adjust(top=0.85)
    plt.title(f"Objective value of the restart\n{algorithm} algorithm on the\nredistribution of lessons (N = {N})")
    plt.savefig(f"output_data/{algorithm}_{dt_string}_plot.png", dpi=300)
    