import platform
if platform.system() == "Darwin":
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib import pyplot as plt
else:
    import matplotlib.pyplot as plt

def visualize_hillclimber(list_of_points, finetune=False):

    plt.figure()

    N = len(list_of_points)
    
    iterations = range(N)
    malus_points = list_of_points
    
    plt.plot(iterations, malus_points)
    plt.xlabel("No. of iterations")
    plt.ylabel("Objective value")
    plt.subplots_adjust(top=0.85)

    if not finetune: # restart hc
        plt.title(f"Objective value of the restart\nhillclimber algorithm on the\nredistribution of lessons (N = {N})")
        plt.savefig("output_data/restart_hillclimber_plot.png", dpi=300)
    else: # redistribute students
        plt.title(f"Objective value of the hillclimber\nalgorithm after redistributing students\n(N = {N})")
        plt.savefig("output_data/redistribute_hillclimber_plot.png", dpi=300)

# Kunnen we niet picklen nu nog?