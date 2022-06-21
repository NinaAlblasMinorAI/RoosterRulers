import numpy as np
from bokeh.plotting import figure, show, save, output_file
from bokeh.io import output_notebook
from bokeh.models import ColumnDataSource, Grid, LinearAxis, Plot, Rect, Text, HoverTool, Ticker
import pandas as pd
from code.classes.schedule import Schedule
from code.classes.lesson import Lesson
import itertools

def get_all_empty_slots(schedule_obj):

    unused_slots = [(row, column) for row, column in zip(*np.where(schedule_obj.get_dataframe().values == "-"))]

    return schedule_obj.get_empty_slots() + unused_slots

def remove_empty_slots(x_vals, y_vals, empty_slots):
    for i, (y, x) in enumerate(list(zip(y_vals - 0.5, x_vals))[::-1]):
        if (y, x) in empty_slots:
            print("coords: ", y, x)
            np.delete(x_vals, i)
            np.delete(y_vals, i)

    return x_vals, y_vals + 0.5

x_values = np.tile(np.arange(7), 5)     # 0 1 2 3 4 5 6 0 1 2 3 4 5 6 ...
y_values = np.repeat(np.arange(5) + .5, 7)   # 0.5 0.5 0.5 0.5 0.5 0.5 0.5 1.5 1.5 1.5 1.5 1.5 1.5 1.5 ...

test_schedule = Schedule()
print(test_schedule.get_dataframe())
all_empty_slots = get_all_empty_slots(test_schedule)
print("empty slots: ", all_empty_slots)

# loop over the days
for i in range(0, 25, 5):
    # one day's lessons     
    df = test_schedule.get_dataframe().iloc[i:i+5]

    lesson_types_df = df.applymap(lambda lesson_obj:lesson_obj.get_type() if isinstance(lesson_obj, Lesson) else "")
    bla = list(itertools.chain(*lesson_types_df.values.tolist()))
    print("List1: ", bla)
    bla = list(filter(lambda val: val !=  "", bla))

    print("List2: ", bla, "\n")

    # print("x: ", x_values)
    # print("y: ", y_values + i)

    # new_x, new_y = remove_empty_slots(x_values, y_values + i, all_empty_slots)

    # print("Removing empty slots...")

    # print("New x:", new_x)
    # print("New y:", new_y)