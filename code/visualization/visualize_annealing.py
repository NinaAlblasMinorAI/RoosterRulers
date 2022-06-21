import platform
if platform.system() == "Darwin":
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib import pyplot as plt
else:
    import matplotlib.pyplot as plt

def visualize_annealing(list_of_points):

    plt.figure()

    N = len(list_of_points)
    
    iterations = range(N)
    malus_points = list_of_points
    
    plt.plot(iterations, malus_points)
    plt.axhline(y = 0, color = 'r', linestyle = ':')
    plt.xlabel("No. of iterations")
    plt.ylabel("Objective value")
    plt.subplots_adjust(top=0.85)

    plt.title(f"Objective value of the simulated\nannealing algorithm on the\nredistribution of lessons (N = {N})")
    plt.savefig("output_data/annealing_lessons_plot.png", dpi=300)