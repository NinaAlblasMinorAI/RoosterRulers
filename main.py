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
    Take a randomly generated schedule and applies
    the hillclimber algorithm to it.
    """

    # run the random algorithm N times
    malus_points_runs = []
    best_malus_points = math.inf
    best_schedule = None

    schedule = Schedule()

    # fill schedule randomly
    create_lessons(schedule)
    place_lessons(schedule, "randomize")

    # compute malus points
    malus_points = schedule.eval_schedule()
    print(f"Random run {i + 1} - Malus points: {malus_points}")

    # if malus_points:
    #     malus_points_runs.append(malus_points)

    #     if malus_points < best_malus_points:
    #         best_malus_points = malus_points
    #         best_schedule = schedule
    #         best_schedule_df = best_schedule.get_dataframe()
    #         best_schedule_df.to_csv("output_data/best_random_schedule.csv")
    
    # visualize_random(malus_points_runs, number_of_runs)

    return schedule

def hillclimber(schedule, number_of_runs):
    print("Running hillclimber")
    
    place_lessons(schedule, "hillclimber")

    # compute malus points
    malus_points = schedule.eval_schedule()
    print(f"Hillclimber run {i + 1} - Malus points: {malus_points}")


if algorithm == "random":
    for i in range(number_of_runs):
        randomize()

if algorithm == "hillclimber":
    for i in range(number_of_runs):
        schedule = randomize()
        hillclimber(schedule, number_of_runs)
    