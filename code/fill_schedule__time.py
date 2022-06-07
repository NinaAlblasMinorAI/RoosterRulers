import pandas as pd
from empty_schedule import build_empty_schedule
from loader import init_courses
import course
import room

# import the empty schedule
schedule = build_empty_schedule()
# print(schedule)

# get a list of courses
courses = init_courses("../data/courses.csv")
# print(courses)

# get a list of rooms from the headers of the schedule
rooms = schedule.columns.values.tolist()

# fill the schedule with courses
x = 0
y = 0
for course in courses:
    number_of_students = course.get_expected_students()
    while number_of_students > rooms[x].get_capacity():
        x += 1
        if x == 7:
            y += 1
            x = 0
    schedule.iloc[y,x]= course.get_expected_students()
    # schedule.iloc[y,x]= course._name
    x += 1
    if x == 7:
        y += 1
        x = 0

# get a list of capacities of the rooms
capacities = []
for room in rooms:
    capacity = room.get_capacity()
    capacities.append(capacity)

# set the headers to the capacities of the rooms
schedule.columns = capacities
print(schedule) 

schedule.to_csv("../data/schedule_time.csv")