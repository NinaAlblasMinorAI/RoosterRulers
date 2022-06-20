import pickle
import argparse

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

# close the file
pickle_input_file.close()