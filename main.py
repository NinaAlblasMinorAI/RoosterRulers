from code.algorithms.redistribute_courses import RedistributeCourses
from code.algorithms.redistribute_lessons import RedistributeLessons
from code.algorithms.redistribute_students import RedistributeStudents
from code.visualization.visualize_box_plot import visualize_box_plot
from code.visualization.visualize_schedule import visualize_schedule
from code.visualization.visualize_iterative import visualize_iterative
from code.classes.schedule import Schedule
from os.path import exists

from datetime import datetime
import argparse
import pickle
import sys
import math


def main(algorithm, nr_runs, nr_optimize_runs, nr_courses, nr_repeats, nr_outer_repeats, nr_inner_repeats, temperature, verbose):    
        
    # check if the maximum number of 11 split lessons is not exceeded
    if ((nr_optimize_runs - 1) * nr_courses) > 11:
        print("only 11 extra lessons can be created")
        return

    # check for a valid algorithm
    if algorithm not in ["random","hillclimber","simulated_annealing"]:
        print("The chosen algorithm must be random, hillclimber or simulated_annealing")
        return
    
    # create a log file with current date and time
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M")
    logfile = open(f"output_data/log_{algorithm}_{dt_string}.txt", "w")  
   
    # create lists to store points for box plot and line graph
    boxplot_points = []
    linegraph_points = []

    # initialize a list to store the best schedule after each run
    best_result = math.inf
    best_results = []

    # build schedule "nr_runs" times and improve if specified
    for i in range(nr_runs):

        # create a random schedule
        schedule = Schedule()

        # improve schedule with specified algorithm, else return the random schedule
        if algorithm == "hillclimber" or algorithm == "simulated_annealing":
            
            # optimize lessons, then optimize students "nr_optimize_runs" times
            # between each run, create extra lessons
            for j in range(nr_optimize_runs):

                # shuffle lessons based on specified algorithm and save points
                print(f"Starting lesson {algorithm} run {i + 1} optimize run {j + 1}.....")
                lesson_swap = RedistributeLessons(algorithm, schedule, nr_repeats, temperature, verbose) 
                linegraph_points.extend(lesson_swap.get_points())
                schedule = lesson_swap.get_schedule()
                logfile.write(f"Intermediate result after shuffling lessons: {schedule.eval_schedule()}\n")

                # shuffle students between lessons with hillclimber and save points
                print(f"Starting student hillclimber run {i + 1} optimize run {j + 1}.....")
                student_swap = RedistributeStudents("hillclimber", schedule, nr_outer_repeats, nr_inner_repeats, verbose)
                linegraph_points.extend(student_swap.get_points())
                schedule = student_swap.get_schedule()
                logfile.write(f"Intermediate result after shuffling students: {schedule.eval_schedule()}\n")
                
                # redistribute courses in lessons with greedy and save points
                # this step is not performed after the last optimize run
                if j != (nr_optimize_runs - 1):
                    print(f"Starting course greedy run {i + 1} optimize run {j + 1}, creating {nr_courses} extra lessons.....")
                    course_split = RedistributeCourses("greedy", schedule, nr_courses, verbose)
                    linegraph_points.extend(course_split.get_points())
                    schedule = course_split.get_schedule()
                    logfile.write(f"Intermediate result after redistributing courses: {schedule.eval_schedule()}\n")                      

        # compute malus points of schedule
        malus_points = schedule.eval_schedule(False)
        schedule.eval_schedule(True)

        # save the schedule if it is the best schedule so far
        if malus_points < best_result:
            best_result = malus_points
            best_results = []
            best_results.append(schedule)

        # print the malus points to the log file
        result_string = f"{algorithm} run {i + 1} - Malus points: {malus_points}\n"
        if verbose:
            print(result_string)
        logfile.write(result_string)
        
        # if the schedule is valid, add the malus points to a the list of results
        if malus_points:
            boxplot_points.append(malus_points)
    
    # close the log file
    logfile.close()
    print(f"log_{algorithm}_{dt_string}.txt created in folder output_data")

    # get the date and time for the output files
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y_%H_%M")

    # actions for the hillclimber and simulated annealing runs
    if algorithm == "hillclimber" or algorithm == "simulated_annealing":
        
        # plot the points
        visualize_iterative(linegraph_points, algorithm)
        print(f"{algorithm}_{dt_string}_plot.png created in folder output_data")
        
        # store the best schedule in a pickle file
        sys.setrecursionlimit(2000)
        pickle_output_file = open(f"output_data/pickled_schedule_{algorithm}_{dt_string}.pickle", "wb")
        pickle.dump(schedule, pickle_output_file)
        pickle_output_file.close()
        print(f"pickled_schedule_{algorithm}_{dt_string}.pickle created in folder output_data")
                    
        # make a bokeh visualization of the best schedule
        visualize_schedule(schedule, f"output_data/{algorithm}_{dt_string}_schedule.html")
        print(f"{algorithm}_{dt_string}_schedule.html created in folder output_data")

        # create a box plot of the last hillclimber and simulated annealing runs
        hc_boxplot_points = []
        if algorithm == "hillclimber":
            box_plot_points_file = open(f"output_data/box_plot_points_{algorithm}.txt", "w") 
            for point in boxplot_points:
                box_plot_points_file.write(f"{point}\n")
            box_plot_points_file.close()
        else:
            if exists("output_data/box_plot_points_hillclimber.txt"):
                with open("output_data/box_plot_points_hillclimber.txt", "r") as f:
                    for line in f:
                        hc_boxplot_points.append(int(line[:-1]))
            
        visualize_box_plot(hc_boxplot_points, boxplot_points, N=nr_runs, T=temperature, R1=nr_repeats, R2=nr_outer_repeats, R3=nr_inner_repeats)
        print(f"{dt_string}_boxplot.png created in folder output_data")

if __name__ == "__main__":

    # set-up parsing command line arguments
    parser = argparse.ArgumentParser(description='Create a university schedule')

    # adding arguments
    parser.add_argument("algorithm", help="algorithm to fill the schedule")
    parser.add_argument("-n", type=int, default=1, dest="nr_runs", help="number of runs")
    parser.add_argument("-O", type=int, default=1, dest="nr_optimize_runs", help="number of optimize runs using extra lessons")
    parser.add_argument("-c", type=int, default=10, dest="nr_courses", help="number of extra lessons to create per optimize run")
    parser.add_argument("-r", type=int, default=100, dest="nr_repeats", help="number of repeats for redistribute lessons ")
    parser.add_argument("-o", type=int, default=10, dest="nr_outer_repeats", help="number of outer repeats for redistribute students")
    parser.add_argument("-i", type=int, default=10, dest="nr_inner_repeats", help="number of inner repeats for redistribute students")
    parser.add_argument("-t", type=float, default=1, dest="temperature", help="simulated annealing start temperature")
    parser.add_argument("-v", default=False, dest="verbosity", help="increase output verbosity", action="store_true")

    # read arguments from command line
    args = parser.parse_args()

    main(args.algorithm, args.nr_runs, args.nr_optimize_runs, args.nr_courses, args.nr_repeats, 
        args.nr_outer_repeats, args.nr_inner_repeats, args.temperature, args.verbosity)

