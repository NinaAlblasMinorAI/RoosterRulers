import pandas as pd
from empty_schedule import build_empty_schedule

test = build_empty_schedule()
print(test)
# # make a list of 
# course_data = pd.read_csv('../data/courses.csv', delimiter=";")
# courses = list(course_data["Vakken voor periode 4"])

# schedule = pd.read_csv('../data/schedule.csv')

# x = 1
# y = 0
# for course in courses:
#     schedule.iloc[y,x]= course
#     x += 1
#     if x == 8:
#         y += 1
#         x = 1

# print(schedule) 

# schedule.to_csv("../data/schedule_baseline.csv")