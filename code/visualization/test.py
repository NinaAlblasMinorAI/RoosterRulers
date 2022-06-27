from visualize_box_plot import visualize_box_plot
from visualize_iterative import visualize_iterative

my_list = [1, 2, 3, 4, 5, 6]

box_plot_points_file = open(f"test_points.txt", "w")      
    
for i in my_list:
    box_plot_points_file.write(f"{i}\n")

box_plot_points_file.close()

# load hillclimber box plot points
hc_boxplot_points = []
with open(f"test_points.txt", "r") as f:
    for line in f:
        hc_boxplot_points.append(int(line[:-1]))

sa_boxplot_points = [20000, 8000, 3000, 1000, 800, 300, 150, 10, 3]

# visualize_box_plot(hc_boxplot_points, sa_boxplot_points, N=10, T=2, R1=20, R2=300, R3=1000)
visualize_iterative(sa_boxplot_points, "hillclimber")
