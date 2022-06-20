from code.algorithms.redistribute_lessons import lesson_hillclimber, lesson_simulated_annealing
from code.algorithms.redistribute_students import student_hillclimber
from code.visualization.visualize_random import visualize_random
from code.visualization.visualize_schedule import visualize_schedule
from code.visualization.visualize_hillclimber import visualize_hillclimber
from code.classes.schedule import Schedule
from datetime import datetime
import argparse
import pickle
import sys
import math

# create a command line argument parser
parser = argparse.ArgumentParser(description='Create a university schedule')
parser.add_argument("algorithm", help="algorithm to fill the schedule")
parser.add_argument("-n", type=int, default=1, dest="number_of_runs", help="number of runs")
parser.add_argument("-r", type=int, default=1, dest="number_of_repeats", help="number of repeats")
parser.add_argument("-v", default=False, dest="verbosity", help="increase output verbosity", action="store_true")

# parse the command line arguments
args = parser.parse_args()

# get the arguments from the command line
algorithm = args.algorithm
number_of_runs = args.number_of_runs
number_of_repeats = args.number_of_repeats
output = args.number_of_repeats
verbose = args.verbosity

# datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")

# create a log file
logfile = open(f"output_data/log_{algorithm}_{dt_string}.txt", "w")

# create a pickle output file if algorithm == "hillclimber" or algorithm ==  "simulated_annealing"
if algorithm == "hillclimber" or algorithm ==  "simulated_annealing":
    pickle_output_file = open(f"output_data/pickled_schedule_{algorithm}_{dt_string}.pickle", "wb")

# initialize an empty list of malus point results for the random_box_plot
malus_points_runs = []

# initialize a empty list of malus points for the hillclimber and simulaten annealing runs
total_points_list = []

# initialize the best result of the runs 
best_result = math.inf

for i in range(number_of_runs):

    # create a random schedule
    schedule = Schedule()

    if algorithm == "hillclimber":
        schedule, points = lesson_hillclimber(schedule, verbose)
        total_points_list.append(points)
        schedule, points = student_hillclimber(schedule, verbose)
        total_points_list.append(points)
        
    if algorithm == "simulated_annealing":
        schedule, points = lesson_simulated_annealing(schedule, verbose)
        total_points_list.append(points)
        schedule, points = student_hillclimber(schedule, verbose)
        total_points_list.append(points)

    # compute and print malus points
    malus_points = schedule.eval_schedule()

    # save the schedule if it is the best schedule so far
    if malus_points < best_result:
        best_result = malus_points
        best_results = []
        best_results.append(schedule)

    # print the malus points
    result_string = f"{algorithm} run {i + 1} - Malus points: {malus_points}\n"
    if verbose:
        print(result_string)
    logfile.write(result_string)
    
    # if algorithm is random_box_plot and the schedule is valid, add the malus points to a the list of results
    if algorithm == "random_box_plot" and malus_points:
            malus_points_runs.append(malus_points)

# if algorithm is random_box_plot, create a box plot of the results
if algorithm == "random_box_plot":
    visualize_random(malus_points_runs, number_of_runs)

# actions for the hillclimber and simulaten annealing runs
if algorithm == "hillclimber" or algorithm ==  "simulated_annealing":
    
    # plot the points
    print(total_points_list)
    visualize_hillclimber(total_points_list, finetune=True)
    print(f"{algorithm}_plot.png created in folder output_data")

    # get the best schedule
    schedule = best_results(0) 
    print(schedule.eval_schedule())

    # store the best schedule in a pickle file
    sys.setrecursionlimit(2000)
    pickle.dump(schedule, pickle_output_file)
        
    # make a bokeh visualization of the best schedule
    visualize_schedule(schedule, f"output_data/{algorithm}_schedule.html")
    print(f"{algorithm}_schedule.html created in folder output_data")

    # close the pickle file
    pickle_output_file.close()

# close the log file
logfile.close()