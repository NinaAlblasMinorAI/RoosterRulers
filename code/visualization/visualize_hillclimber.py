import platform
if platform.system() == "Darwin":
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib import pyplot as plt
else:
    import matplotlib.pyplot as plt

def visualize_restart_hillclimber(list_of_points):
    N = len(list_of_points)
    
    iterations = range(N)
    malus_points = list_of_points
    
    plt.plot(iterations, malus_points)
    plt.xlabel("No. of iterations")
    plt.ylabel("Objective value")
    plt.title(f"Objective value of the valid solutions of the restart hillclimber algorithm (N = {N})")
    plt.title("Results of the restart hillclimber algorithm")

    plt.savefig("output_data/restart_hillclimber_plot.png")