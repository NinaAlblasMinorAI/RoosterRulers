import random
from code.classes import room
from code.classes.lesson import Lesson
from code.classes.room import Room
from code.classes.schedule import Schedule
from code.algorithms.create_lessons import create_lessons
from code.algorithms.place_lessons import place_lessons
from code.visualization.visualize_random import visualize_random

def run_N_times(algorithm, N, room_file, student_file, course_file):
    """
    Runs the specified algorithm N amount
    of times.
    """

    if algorithm == "randomize":

        valid_schedules = {}
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
                valid_schedules[schedule] = malus_points

        visualize_random(valid_schedules.values(), N)