from statistics import mean
from code.algorithms.create_lessons import create_lessons
from code.algorithms.place_lessons import hillclimber, place_lessons
from code.classes.schedule import Schedule
from code.visualization.visualize_random import visualize_random
from copy import deepcopy
import pandas as pd
import math
import random
import argparse
import time
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")

# Create a command line argument parser
parser = argparse.ArgumentParser(description='Create a university schedule')
parser.add_argument("algorithm", help="algorithm to fill the schedule")
parser.add_argument("-n", type=int, default=1, dest="number_of_runs", help="number of runs")

# Parse the command line arguments
args = parser.parse_args()

algorithm = args.algorithm
number_of_runs = args.number_of_runs

def randomize():
    """
    Creates a randomly generated schedule 
    """
    # create a schedule
    schedule = Schedule()

    # fill schedule randomly
    create_lessons(schedule)
    place_lessons(schedule, "randomize")

    # return the schedule
    return schedule

# create random schedules and calculate and print the malus points
if algorithm == "random":
    
    # create a logfile
    logfile = open(f"output_data/random{dt_string}.txt", "w")

    for i in range(number_of_runs):
        
        # create a random schedule
        schedule = randomize()

        # compute and print malus points
        malus_points = schedule.eval_schedule()
        result_string = f"Random run {i + 1} - Malus points: {malus_points}\n"
        print(result_string)
        logfile.write(result_string)

    # close the logfile
    logfile.close()


# create random schedules and create a box plot with the average and minimum malus poinst
if algorithm == "random_maximize":

    # create an empty list of malus point results
    malus_points_runs = []

    # best_malus_points = math.inf
    # best_schedule = None
    for i in range(number_of_runs):

        # create a random schedule
        schedule = randomize()

        # compute the malus points
        malus_points = schedule.eval_schedule()

        # for valid schedules, add the malus points to a the list of results
        if malus_points:
            malus_points_runs.append(malus_points)

            # if malus_points < best_malus_points:
            #     best_malus_points = malus_points
            #     best_schedule = schedule
            #     best_schedule_df = best_schedule.get_dataframe()
            #     best_schedule_df.to_csv("output_data/best_random_schedule.csv")
    
    # create a box plot of the results
    visualize_random(malus_points_runs, number_of_runs)
    print("random_boxplot.png created in folder output_data")

if algorithm == "hillclimber":

    # create a logfile
    logfile = open(f"output_data/hillclimber{dt_string}.txt", "w")

    for i in range(number_of_runs):
        
        # print a message (because there is a waiting time)
        print("Running hillclimber....")
        
        # create a new random schedule
        schedule = randomize()

        # place the lessons according to the hillclimber algorithm
        place_lessons(schedule, "hillclimber")

        # compute malus points
        malus_points = schedule.eval_schedule()
        result_string = f"Hillclimber run {i + 1} - Malus points: {malus_points}\n"
        print(result_string)
        logfile.write(result_string)


    # close the logfile
    logfile.close()
    