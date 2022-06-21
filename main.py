from code.algorithms.redistribute_courses import course_greedy
from code.algorithms.redistribute_lessons import lesson_hillclimber, lesson_simulated_annealing
from code.algorithms.redistribute_students import student_hillclimber
from code.visualization.visualize_box_plot import visualize_box_plot
from code.visualization.visualize_schedule import visualize_schedule
from code.visualization.visualize_iterative import visualize_iterative
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
parser.add_argument("-r", type=int, default=10, dest="number_of_repeats", help="number of repeats")
parser.add_argument("-o", type=int, default=10, dest="number_of_outer_repeats", help="number of outer repeats for redistribute students")
parser.add_argument("-i", type=int, default=10, dest="number_of_inner_repeats", help="number of inner repeats for redistribute students")
parser.add_argument("-v", default=False, dest="verbosity", help="increase output verbosity", action="store_true")

# parse the command line arguments
args = parser.parse_args()

# get the arguments from the command line
algorithm = args.algorithm
number_of_runs = args.number_of_runs
number_of_repeats = args.number_of_repeats
number_of_outer_repeats = args.number_of_outer_repeats
number_of_inner_repeats = args.number_of_inner_repeats
verbose = args.verbosity

# set the time and date for output files
now = datetime.now()
dt_string = now.strftime("%d_%m_%Y_%H_%M")

# create a log file with current date and time
logfile = open(f"output_data/log_{algorithm}_{dt_string}.txt", "w")

# create a pickle output file if algorithm is hillclimber or simulated_annealing
if algorithm == "hillclimber" or algorithm ==  "simulated_annealing":
    pickle_output_file = open(f"output_data/pickled_schedule_{algorithm}_{dt_string}.pickle", "wb")

# initialize an empty list of malus point results for the box_plot
malus_points_runs = []

# initialize a empty list of malus points for the hillclimber and simulated annealing plots
total_points_list = []

# initialize the best result of the runs 
best_result = math.inf

for i in range(number_of_runs):

    # create a random schedule
    schedule = Schedule()

    # start the allocation of lessons over the schedule using hillclimber or simulated annealing
    if algorithm == "hillclimber" or algorithm == "simulated_annealing":
        if algorithm == "hillclimber":
            print(f"Starting lesson hillclimber run {i}.....")
            schedule, points = lesson_hillclimber(schedule, number_of_repeats, verbose)
        else:
            print(f"Starting lesson simulated annealing run {i}.....")
            schedule, points = lesson_simulated_annealing(schedule, number_of_repeats, verbose)
        total_points_list.extend(points)

        # compute and print malus points
        malus_points = schedule.eval_schedule()
        logfile.write(f"Intermediate result: {malus_points}\n")

        # start the allocation of students over the lessons
        print(f"Starting student hillclimber run {i}.....")
        schedule, points = student_hillclimber(schedule, number_of_outer_repeats, number_of_inner_repeats, verbose)
        total_points_list.extend(points)

        schedule = course_greedy(schedule)
        schedule, points = lesson_simulated_annealing(schedule, number_of_repeats, verbose)
        schedule, points = student_hillclimber(schedule, number_of_outer_repeats, number_of_inner_repeats, verbose)

        
    # compute malus points
    malus_points = schedule.eval_schedule()
    schedule.eval_schedule_objects()

    # save the schedule if it is the best schedule so far
    if malus_points < best_result:
        best_result = malus_points
        best_results = []
        best_results.append(schedule)

    # print the malus points to the log file
    result_string = f"{algorithm} run {i + 1} - Malus points: {malus_points}\n"
    if verbose:
        print(result_string)
    logfile.write(result_string)
    
    # if the schedule is valid, add the malus points to a the list of results
    if malus_points:
            malus_points_runs.append(malus_points)

# create a box plot of the results
visualize_box_plot(malus_points_runs, number_of_runs)
print("box_plot.png created in folder output_data")

# actions for the hillclimber and simulaten annealing runs
if algorithm == "hillclimber" or algorithm ==  "simulated_annealing":
    
    # plot the points
    visualize_iterative(total_points_list, algorithm)
    print(f"{algorithm}_{dt_string}_plot.png created in folder output_data")
    
    # get the best schedule
    schedule = best_results[0] 
    
    # store the best schedule in a pickle file
    sys.setrecursionlimit(2000)
    pickle.dump(schedule, pickle_output_file)
        
    # make a bokeh visualization of the best schedule
    visualize_schedule(schedule, f"output_data/{algorithm}_{dt_string}_schedule.html")
    print(f"{algorithm}_{dt_string}_schedule.html created in folder output_data")

    # close the pickle file
    pickle_output_file.close()

# close the log file
logfile.close()

# # REMOVE
# test_schedule = Schedule()
# visualize_schedule(test_schedule, "output_data/random_schedule.html")
# print("random_schedule.html created in output_data folder")