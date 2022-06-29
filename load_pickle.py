"""
- Programmeertheorie
- RoosterRulers - Lectures & Lesroosters

Program to get a pickled schedule object, print the malus points and generate a csv file 
and a Bokeh plot
"""

import pickle
import argparse
from datetime import datetime

from code.visualization.visualize_schedule import visualize_schedule

parser = argparse.ArgumentParser(description='Load a pickled schedule object')
parser.add_argument("input_file")

# Parse the command line arguments
args = parser.parse_args()
input_file = args.input_file

# retrieving the pickled schedule object
pickle_input_file = open(f"output_data/{input_file}", "rb")

# get the schedule from the file
schedule = pickle.load(pickle_input_file)

# print the malus points
print(f"Malus points: {schedule.eval_schedule()}")

# get the date and time for the output files
now = datetime.now()
dt_string = now.strftime("%d_%m_%Y_%H_%M")

# make a bokeh visualization of the best schedule
visualize_schedule(schedule, f"output_data/{dt_string}_schedule.html")
print(f"{dt_string}_schedule.html created in folder output_data")

# output the best schedule to csv
schedule.print_csv(dt_string)
print(f"result_{dt_string}.csv created in folder output_data")

# close the file
pickle_input_file.close()