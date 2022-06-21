import pickle
import argparse

from code.visualization.visualize_schedule import visualize_schedule

parser = argparse.ArgumentParser(description='Load a pickled schedule object')
parser.add_argument("input_file")

# Parse the command line arguments
args = parser.parse_args()

input_file = args.input_file

# retrieving the pickled schedule object
pickle_input_file = open(f"output_data/{input_file}", "rb")

# dump information to that file
pickled_schedule_obj = pickle.load(pickle_input_file)

print(pickled_schedule_obj.get_dataframe())
visualize_schedule(pickled_schedule_obj, "output_data/test.html")
lessons = pickled_schedule_obj.get_lessons()
result_file = open(f"output_data/result.csv", "w")
result_file.write("student,course,activity,room,day,time\n")
for lesson in lessons:
    students = lesson.get_students()
    for student in students:
        result_string = f"{student._name},{lesson}\n"
        result_file.write(result_string)

result_file.close()

# close the file
pickle_input_file.close()