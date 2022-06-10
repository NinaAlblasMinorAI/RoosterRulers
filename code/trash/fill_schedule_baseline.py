import pandas as pd

# make a list of of courses from a csv file
course_data = pd.read_csv('../input_data/courses.csv')
courses = list(course_data["Vak"])

# get the schedule from a csv file
schedule = pd.read_csv('../output_data/schedule.csv')

# loop over the slots, start with x = 1 because 0 is for the time description
x = 1
y = 0
for course in courses:
    schedule.iloc[y,x]= course
    x += 1
    # at the end of a row, start at a new row
    if x == 8:
        y += 1
        x = 1

# print to the screen
print(schedule) 

# write to the output_data folder
schedule.to_csv("../output_data/schedule_baseline.csv")