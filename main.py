from statistics import mean
from code.algorithms.create_lessons import create_lessons
from code.algorithms.place_lessons import place_lessons
from code.classes.schedule import Schedule
from code.algorithms.run_N_times import run_N_times
import random

# build emtpy schedule
room_file = ("input_data/rooms.csv")
student_file = ("input_data/students.csv")
course_file = ("input_data/courses.csv")

# run the random algorithm 1000 times
run_N_times("randomize", 1000, room_file, student_file, course_file)

# # visualize schedule
# visualize_schedule(schedule)