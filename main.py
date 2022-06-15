from statistics import mean
from code.algorithms.create_lessons import create_lessons
from code.algorithms.place_lessons import hillclimber, place_lessons
from code.classes.schedule import Schedule
from code.visualization.visualize_random import visualize_random
import pandas as pd
import math
import random

# build emtpy schedule
room_file = ("input_data/rooms.csv")
student_file = ("input_data/students.csv")
course_file = ("input_data/courses.csv")

# TODO: dit hieronder in 1 functie schrijven?

# run the random algorithm 1000 times
malus_points_runs = []
best_malus_points = math.inf
best_schedule = None

N = 1000

for i in range(N):
    schedule = Schedule(room_file, student_file, course_file)

    # fill schedule randomly
    lessons = create_lessons(schedule.get_courses())
    schedule.add_lessons(lessons)
    place_lessons(schedule, lessons, "randomize")

    # compute malus points
    malus_points = schedule.eval_schedule()
    print(f"Run {i + 1} - Malus points: {malus_points}")

    if malus_points:
        malus_points_runs.append(malus_points)

        if malus_points < best_malus_points:
            best_malus_points = malus_points
            best_schedule = schedule.get_dataframe()
            best_schedule.to_csv("output_data/best_random_schedule.csv")

visualize_random(malus_points_runs, N)

# run the hillclimber algorithm with a randomly filled in schedule (the best one?)
place_lessons(schedule, lessons, "hillclimber")

# compute malus points
malus_points = schedule.eval_schedule()
print(f"Run {i + 1} - Malus points: {malus_points}")

# visualize_random(malus_points_runs, N)

# # visualize schedule
# visualize_schedule(schedule)