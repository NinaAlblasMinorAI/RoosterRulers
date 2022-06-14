from statistics import mean
from code.algorithms.create_lessons import create_lessons
from code.algorithms.place_lessons import place_lessons
from code.classes.schedule import Schedule
import random

# build emtpy schedule
room_file = ("input_data/rooms.csv")
student_file = ("input_data/students.csv")
course_file = ("input_data/courses.csv")

valid_schedules = {}
for i in range(1000):
    schedule = Schedule(room_file, student_file, course_file)

    # fill schedule randomly
    lessons = create_lessons(schedule.get_courses())
    schedule.add_lessons(lessons)
    place_lessons(schedule, lessons, "randomize")

    # compute malus points
    malus_points = schedule.eval_schedule()
    print(malus_points)

    if malus_points:
        valid_schedules[schedule] = malus_points

average = mean(valid_schedules.values())
minimum = min(valid_schedules.values())

print(average, minimum)

# visualize schedule
# visualize_schedule(schedule)