import pandas as pd
import loader

rooms = loader.init_rooms("../data/rooms.csv")
courses = loader.init_courses("../data/courses.csv")
students = loader.init_students("../data/students.csv", courses)

# TODO: sommige namen geven error
# studenten_data = pd.read_csv("data/studentenvakken.csv", delimiter=",")

timeslots = ["Monday 09:00-11:00", "11:00-13:00", "13:00-15:00", "15:00-17:00", 
             "Tuesday 09:00-11:00", "11:00-13:00", "13:00-15:00", "15:00-17:00", 
             "Wednesday 09:00-11:00", "11:00-13:00", "13:00-15:00", "15:00-17:00", 
             "Thurday 09:00-11:00", "11:00-13:00", "13:00-15:00", "15:00-17:00", 
             "Friday 09:00-11:00", "11:00-13:00", "13:00-15:00", "15:00-17:00", ]

data = pd.DataFrame(index = timeslots, columns=rooms, data=0)

# # welke lokalen vrij op maandag 9-11?
# sub_df = (data.iloc[0] == 0)
# print(sub_df)

data.to_csv("../data/schedule.csv")