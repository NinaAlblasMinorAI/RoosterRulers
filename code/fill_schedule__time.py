import pandas as pd
from empty_schedule import build_empty_schedule
from loader import init_students, init_courses
import course

# import the empty schedule
schedule = build_empty_schedule()

# get a list of courses
students = init_students("../data/students.csv")
courses = init_courses("../data/courses.csv", students)

# get a list of rooms from the headers of the schedule
rooms = schedule.columns.values.tolist()

# fill the schedule with courses
x = 0
y = 0
for course in courses:
    # get the number of students in the course
    number_of_students = course.get_expected_students()

    # if the course does not fit in the room, go to the next one
    while number_of_students > rooms[x].get_capacity():
        x += 1

        # after the last room, go to the next time slot
        if x == 7:
            y += 1
            x = 0
    
    # add the course to the schedule
    schedule.iloc[y,x]= course
    
    # go to the next room
    x += 1
    if x == 7:
        y += 1
        x = 0

print(schedule)
# schedule.to_csv("../data/schedule_time.csv")