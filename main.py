from statistics import mean
from code.algorithms.create_lessons import create_lessons
from code.algorithms.place_lessons import hillclimber, place_lessons
from code.classes.schedule import Schedule
from code.visualization.visualize_random import visualize_random
from copy import deepcopy
import pandas as pd
import math
import random


# run the random algorithm N times
malus_points_runs = []
best_malus_points = math.inf
best_schedule = None

schedules = []
N = 20

for i in range(N):
    schedule = Schedule()

    # fill schedule randomly
    create_lessons(schedule)
    random_schedule = place_lessons(schedule, "randomize")

    # compute malus points
    malus_points = random_schedule.eval_schedule()
    print(f"Run {i + 1} - Malus points: {malus_points}")

    schedules.append(random_schedule)

    # if malus_points:
    #     malus_points_runs.append(malus_points)

    #     if malus_points < best_malus_points:
    #         best_malus_points = malus_points
    #         best_schedule = schedule
    #         best_schedule_df = best_schedule.get_dataframe()
    #         best_schedule_df.to_csv("output_data/best_random_schedule.csv")

# visualize_random(malus_points_runs, N)

# # run the hillclimber algorithm with a randomly filled in schedule
# best_schedule = place_lessons(schedules[0], "hillclimber")

# # compute malus points
# malus_points = best_schedule.eval_schedule()
# print(f"Best schedule - Malus points: {malus_points}")

# run the restart hillclimber algorithm with a randomly filled in schedules
best_schedule = place_lessons(schedules, "restart hillclimber")

# compute malus points
malus_points = best_schedule.eval_schedule()
print(f"Best schedule - Malus points: {malus_points}")
