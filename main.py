from code.algorithms.redistribute_courses import RedistributeCourses
from code.algorithms.redistribute_lessons import RedistributeLessons
from code.algorithms.redistribute_students import RedistributeStudents
from code.visualization.visualize_box_plot import visualize_box_plot
from code.visualization.visualize_schedule import visualize_schedule
from code.visualization.visualize_iterative import visualize_iterative
from code.classes.schedule import Schedule
from copy import deepcopy

from datetime import datetime
import argparse
import pickle
import sys
import math


def main(algorithm, nr_runs, nr_repeats, nr_outer_repeats, nr_inner_repeats, temperature, nr_courses, verbose):

    # set the time and date for output files
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M")

    # create a log file with current date and time
    logfile = open(f"output_data/log_{algorithm}_{dt_string}.txt", "w")        

    # lists to store points for box plot and line graph
    boxplot_points = []
    linegraph_points = []

    # initialize list to store best schedules after each run
    best_result = math.inf
    best_results = []

    # build schedule N times and improve if specified
    for i in range(nr_runs):

        # create a random schedule
        schedule = Schedule()

        # improve schedule with specified algorithm, else return the random schedule
        if algorithm == "hillclimber" or algorithm == "simulated_annealing":

            # shuffle lessons based on specified algorithm and save points
            print(f"Starting lesson {algorithm} run {i + 1}.....")
            lesson_swap = RedistributeLessons(algorithm, schedule, nr_repeats, temperature, verbose)
            schedule, points = lesson_swap.get_schedule(), lesson_swap.get_points()
            linegraph_points.extend(points)
            malus_points = schedule.eval_schedule()
            logfile.write(f"Intermediate result after shuffling lessons: {malus_points}\n")

            # shuffle students between lessons with hillclimber and save points
            print(f"Starting student hillclimber run {i + 1}.....")
            student_swap = RedistributeStudents("hillclimber", schedule, nr_outer_repeats, nr_inner_repeats, verbose)
            schedule, points = student_swap.get_schedule(), student_swap.get_points()
            linegraph_points.extend(points)
            malus_points = schedule.eval_schedule()
            logfile.write(f"Intermediate result after shuffling students: {malus_points}\n")

            # redistribute courses in lessons with greedy and save points
            print(f"Starting course greedy run {i + 1}.....")
            course_split = RedistributeCourses("greedy", schedule, nr_courses, verbose)
            schedule, points = course_split.get_schedule(), course_split.get_points()
            linegraph_points.extend(points)
            malus_points = schedule.eval_schedule()
            logfile.write(f"Intermediate result after redistributing courses: {malus_points}\n")

            # shuffle lessons based on specified algorithm and save points
            print(f"Starting lesson {algorithm} run {i + 1}.....")
            lesson_swap = RedistributeLessons(algorithm, schedule, nr_repeats, temperature, verbose)
            schedule, points = lesson_swap.get_schedule(), lesson_swap.get_points()
            linegraph_points.extend(points)
            malus_points = schedule.eval_schedule()
            logfile.write(f"Intermediate result after shuffling lessons: {malus_points}\n")

            # shuffle students between lessons with hillclimber and save points
            print(f"Starting student hillclimber run {i + 1}.....")
            student_swap = RedistributeStudents("hillclimber", schedule, nr_outer_repeats, nr_inner_repeats, verbose)
            schedule, points = student_swap.get_schedule(), student_swap.get_points()
            linegraph_points.extend(points)
            malus_points = schedule.eval_schedule()
            logfile.write(f"Intermediate result after shuffling students: {malus_points}\n")

        # compute malus points of schedule
        malus_points = schedule.eval_schedule()
        schedule.eval_schedule_objects()

        # save the schedule if it is the best schedule so far
        if malus_points < best_result:
            best_result = malus_points
            best_results.append(schedule)

        # print the malus points to the log file
        result_string = f"{algorithm} run {i + 1} - Malus points: {malus_points}\n"
        if verbose:
            print(result_string)
        logfile.write(result_string)
        
        # if the schedule is valid, add the malus points to a the list of results
        if malus_points:
            boxplot_points.append(malus_points)

    # create a box plot of the results
    visualize_box_plot(boxplot_points, nr_runs)
    print(f"{dt_string}_box_plot.png created in folder output_data")

    # actions for the hillclimber and simulated annealing runs
    if algorithm == "hillclimber" or algorithm == "simulated_annealing":
        
        # plot the points
        visualize_iterative(linegraph_points, algorithm)
        print(f"{algorithm}_{dt_string}_plot.png created in folder output_data")
        
        # get the best schedule
        schedule = best_results[0] 
        
        # store the best schedule in a pickle file
        sys.setrecursionlimit(2000)
        pickle_output_file = open(f"output_data/pickled_schedule_{algorithm}_{dt_string}.pickle", "wb")
        pickle.dump(schedule, pickle_output_file)
            
        # make a bokeh visualization of the best schedule
        visualize_schedule(schedule, f"output_data/{algorithm}_{dt_string}_schedule.html")
        print(f"{algorithm}_{dt_string}_schedule.html created in folder output_data")

        # close the pickle file
        pickle_output_file.close()

    # close the log file
    logfile.close()


if __name__ == "__main__":

    # set-up parsing command line arguments
    parser = argparse.ArgumentParser(description='Create a university schedule')

    # adding arguments
    parser.add_argument("algorithm", help="algorithm to fill the schedule")
    parser.add_argument("-n", type=int, default=1, dest="nr_runs", help="number of runs")
    parser.add_argument("-r", type=int, default=10, dest="nr_repeats", help="number of repeats")
    parser.add_argument("-o", type=int, default=10, dest="nr_outer_repeats", help="number of outer repeats for redistribute students")
    parser.add_argument("-i", type=int, default=10, dest="nr_inner_repeats", help="number of inner repeats for redistribute students")
    parser.add_argument("-c", type=int, default=10, dest="nr_courses", help="number of courses to further divide into lessons")
    parser.add_argument("-t", type=int, default=1, dest="temperature", help="simulated annealing start temperature")
    parser.add_argument("-v", default=False, dest="verbosity", help="increase output verbosity", action="store_true")

    # read arguments from command line
    args = parser.parse_args()

    # run main with provided arguments
    main(args.algorithm, args.nr_runs, args.nr_repeats, 
        args.nr_outer_repeats, args.nr_inner_repeats, 
        args.temperature, args.nr_courses, args.verbosity)
