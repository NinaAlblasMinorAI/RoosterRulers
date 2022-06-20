from statistics import mean
from code.algorithms.redistribute_lessons import redistribute_lessons
from code.algorithms.redistribute_students import redistribute_students
from code.classes.schedule import Schedule
from code.visualization.visualize_random import visualize_random
from code.visualization.visualize_schedule import visualize_schedule
from copy import deepcopy
import pandas as pd
import math
import random
import argparse
import time
from datetime import datetime
import pickle


# datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")

# Create a command line argument parser
parser = argparse.ArgumentParser(description='Create a university schedule')
parser.add_argument("algorithm", help="algorithm to fill the schedule")
parser.add_argument("-n", type=int, default=1, dest="number_of_runs", help="number of runs")
# parser.add_argument("-v", default=False, dest="verbose keyword", help="verbose keyword")

# Parse the command line arguments
args = parser.parse_args()

algorithm = args.algorithm
number_of_runs = args.number_of_runs

pickle_output_file = open(f"output_data/pickled_schedule_{algorithm}_{dt_string}.pickle", "wb")

# create random schedules and calculate and print the malus points
if algorithm == "random":
    
    # create a logfile
    logfile = open(f"output_data/random{dt_string}.txt", "w")

    for i in range(number_of_runs):
        
        # create a random schedule
        random_schedule = Schedule()

        # compute and print malus points
        malus_points = random_schedule.eval_schedule()
        result_string = f"Random run {i + 1} - Malus points: {malus_points}\n"
        print(result_string)
        logfile.write(result_string)

    # close the logfile
    logfile.close()

# create random schedules and create a box plot with the average and minimum malus poinst
if algorithm == "random_box_plot":

    # create an empty list of malus point results
    malus_points_runs = []

    for i in range(number_of_runs):

        # create a random schedule
        random_schedule = Schedule()

        # store the schedule in a pickle file
        pickle.dump(best_schedule, pickle_output_file)

        # compute the malus points
        malus_points = random_schedule.eval_schedule()

        # for valid schedules, add the malus points to a the list of results
        if malus_points:
            malus_points_runs.append(malus_points)
    
    # create a box plot of the results
    visualize_random(malus_points_runs, number_of_runs)
    print("random_boxplot.png created in folder output_data")

if algorithm == "hillclimber":

    # create a logfile
    logfile = open(f"output_data/hillclimber{dt_string}.txt", "w")

    random_schedules = []
    for i in range(number_of_runs):
        
        # create a new random schedule
        random_schedule = Schedule()
        random_schedules.append(random_schedule)

    # shuffle lessons and students according to the hillclimber algorithm
    best_schedule = redistribute_lessons(random_schedules, "restart_hillclimber")
    best_schedule = redistribute_students(best_schedule, "hillclimber")

    # store the schedule in a pickle file
    pickle.dump(best_schedule, pickle_output_file)

    # compute malus points
    malus_points = best_schedule.eval_schedule()
    result_string = f"Hillclimber run {i + 1} - Malus points: {malus_points}\n"
    print(result_string)
    logfile.write(result_string)

    # make a bokeh visualization of the schedule
    visualize_schedule(best_schedule, "output_data/schedule.html")

    # close the logfile
    logfile.close()

if algorithm == "simulated_annealing":

    # create a logfile
    logfile = open(f"output_data/simulated_annealing{dt_string}.txt", "w")
    for i in range(number_of_runs):
        random_schedule = Schedule()

        # place the lessons according to the simulated annealing algorithm
        # print a message (because there is a waiting time)
        print("Running simulated annealing (place_lessons)....")
        schedule = redistribute_lessons(random_schedule, "simulated_annealing")
        print("Running hillclimber (redistribute_students)....")
        schedule = redistribute_students(schedule, "hillclimber")

    schedule.eval_schedule_elements()

    # store the schedule in a pickle file
    pickle.dump(schedule, pickle_output_file)

    # make a bokeh visualization of the schedule
    visualize_schedule(schedule, "output_data/annealed_schedule.html")
    
    # compute malus points
    malus_points = schedule.eval_schedule()
    result_string = f"Simulated annealing run - Malus points: {malus_points}\n"
    print(result_string)
    logfile.write(result_string)

    # close the logfile
    logfile.close()
    
# close the pickle file
pickle_output_file.close()