import platform
if platform.system() == "Darwin":
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib import pyplot as plt
else:
    import matplotlib.pyplot as plt

def visualize_hillclimber(list_of_points, finetune=False):
    """
    Visualizes the iterations of the hillclimber algorithm with
    its corresponding malus points. Finetune is False when redistributing
    lessons, and True when redistributing students.
    """

    plt.figure()

    N = len(list_of_points)
    
    iterations = range(N)
    malus_points = list_of_points
    
    plt.plot(iterations, malus_points)
    plt.axhline(y = 0, color = 'r', linestyle = ':')
    plt.xlabel("No. of iterations")
    plt.ylabel("Objective value")
    plt.subplots_adjust(top=0.85)

    # redistribute lessons
    if not finetune: 
        plt.title(f"Objective value of the restart\nhillclimber algorithm on the\nredistribution of lessons (N = {N})")
        plt.savefig("output_data/restart_hillclimber_plot.png", dpi=300)
        
    # redistribute students
    else: 
        plt.title(f"Objective value of the hillclimber\nalgorithm after redistributing students\n(N = {N})")
        plt.savefig("output_data/redistribute_hillclimber_plot.png", dpi=300)