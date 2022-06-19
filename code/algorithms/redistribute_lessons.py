import random
from code.visualization.visualize_hillclimber import visualize_hillclimber


def redistribute_lessons(schedule, algorithm):
    """
    Adds all lessons of a course to the schedule
    according to specified algorithm.
    """

    if algorithm == "hillclimber":
        new_schedule, points = hillclimber(schedule)
    elif algorithm == "restart_hillclimber":
        new_schedule = restart_hillclimber(schedule)

    return new_schedule


def hillclimber(schedule):
    """
    Take a randomly generated schedule and applies
    the hillclimber algorithm to it.
    """

    # hillclimber stops when the number of malus points does not decrease after <threshold> times
    threshold = 1000
    counter = 0

    # variables to keep track of malus points of old and new schedule
    old_points = schedule.eval_schedule()
    new_points = 0

    # keep track of the points in a list
    list_of_points = [old_points]

    timeslot_list = list(schedule.get_timeslots().values())

    while counter < threshold:

        # get two random locations in the schedule
        random_loc1 = 0
        random_loc2 = 0

        while random_loc1 == random_loc2:
            random_loc1 = random.choice(timeslot_list)
            random_loc2 = random.choice(timeslot_list)

        # swap the contents of the random locations
        schedule.swap_contents(random_loc1, random_loc2)

        # obtain malus points of new schedule
        new_points = schedule.eval_schedule()

        # print(f"New points: {new_points}  |  Lowest points: {old_points}")

        if new_points >= old_points:
            schedule.swap_contents(random_loc2, random_loc1)
            counter += 1
        else:
            old_points = new_points
            counter = 0

        list_of_points.append(old_points)

    return schedule, list_of_points


def restart_hillclimber(schedules):
    """
    TO DO.
    """

    total_points_list = []


    best_values = []

    for schedule in schedules:
        best_schedule, list_of_points = hillclimber(schedule)
        malus_points = best_schedule.eval_schedule()
        best_values.append(malus_points)
        total_points_list.extend(list_of_points)

    min_value = min(best_values)
    min_index = best_values.index(min_value)

    # plot the malus points
    visualize_hillclimber(total_points_list)
    print("restart_hillclimber_plot.png created in folder output_data")

    return schedules[min_index]
 

