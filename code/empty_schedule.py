import pandas as pd
from loader import init_rooms


def build_empty_schedule():

    # load in lists of all room objects
    rooms = init_rooms("../input_data/rooms.csv")
    rooms.sort(key=lambda x: x._capacity)
    
    # build list of all possible time slots
    timeslots = ["Monday 09:00-11:00", "11:00-13:00", "13:00-15:00", "15:00-17:00", 
                "Tuesday 09:00-11:00", "11:00-13:00", "13:00-15:00", "15:00-17:00", 
                "Wednesday 09:00-11:00", "11:00-13:00", "13:00-15:00", "15:00-17:00", 
                "Thurday 09:00-11:00", "11:00-13:00", "13:00-15:00", "15:00-17:00", 
                "Friday 09:00-11:00", "11:00-13:00", "13:00-15:00", "15:00-17:00", ]

    # build schedule and return
    schedule = pd.DataFrame(index = timeslots, columns=rooms, data=0)
    return schedule

# # save schedule
# schedule.to_csv("../data/schedule.csv")

# # welke lokalen vrij op maandag 9-11?
# sub_df = (data.iloc[0] == 0)
# print(sub_df)
