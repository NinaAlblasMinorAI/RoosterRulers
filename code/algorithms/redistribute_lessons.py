import random
from code.visualization.visualize_hillclimber import visualize_hillclimber


def redistribute_lessons(schedule, algorithm):
    """
    Shuffles all lessons according to specified algorithm.
    """

    if algorithm == "hillclimber":
        new_schedule, points = hillclimber(schedule)
    elif algorithm == "restart_hillclimber":
        new_schedule = restart_hillclimber(schedule)
    elif algorithm == "simulated_annealing":
        new_schedule = simulated_annealing(schedule)

    return new_schedule


def hillclimber(schedule):
    """
    Applies the hillclimber algorithm to a schedule.
    """

    # hillclimber stops when the number of malus points does not decrease after <threshold> times
    threshold = 1000
    counter = 0

    # variables to keep track of malus points of old and new schedule
    old_points = schedule.eval_schedule()
    new_points = 0

    # keep track of the points in a list
    list_of_points = [old_points]

    while counter < threshold:

        # get two random locations in the schedule
        random_loc1 = schedule.get_random_loc()
        random_loc2 = schedule.get_random_loc()

        # swap the contents of the random locations
        schedule.swap_contents(random_loc1, random_loc2)

        # obtain malus points of new schedule
        new_points = schedule.eval_schedule()

        # print(f"New points: {new_points}  |  Lowest points: {old_points}")

        if new_points > old_points:
            schedule.swap_contents(random_loc2, random_loc1)
            counter += 1
        elif new_points == old_points:
            counter += 1
        else:
            old_points = new_points
            counter = 0

        list_of_points.append(old_points)

    return schedule, list_of_points


def restart_hillclimber(schedules):
    """
    Applies the restart hillclimber algorithm to a schedule.
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


def simulated_annealing(schedule):
    """
    Applies the simulated annealing algorithm to a schedule.
    """
    
    # set the start temperature 
    start_temperature = 0.5
    temperature = start_temperature

    # simulated annealing stops after <threshold> times
    repeats = 20000
    counter = 0
    
    # variables to keep track of malus points of old and new schedule
    old_points = schedule.eval_schedule()
    new_points = 0

    # keep track of the points
    list_of_points = [old_points]

    # run as long as the repeats are not reached, and the temperature is above 0.01 (to avoid dumps)
    while counter < repeats and temperature > 0.01:
    
        # get two random locations in the schedule
        random_loc1 = schedule.get_random_loc()
        random_loc2 = schedule.get_random_loc()

        # swap the contents of the random locations
        schedule.swap_contents(random_loc1, random_loc2)

        # obtain malus points of new schedule
        new_points = schedule.eval_schedule()

        # print the new and old points
        # print(f"New points: {new_points}  |  Lowest points: {old_points}")

        # get a random number between 0 and 1
        random_number = random.random()
        
        # calculate the change based on the old points, new points and temperature
        # use try-except, because there is an overflow if the difference between old and new points is too large
        try:
            # calculate the chance
            chance = 2 ** ((old_points - new_points) / temperature)

            # if the random number is higher than the chance, reverse the swap, else set the new point total
            if random_number > chance:
                schedule.swap_contents(random_loc2, random_loc1)
            else:
                old_points = new_points
        except OverflowError as e:
            print("OverFlowError: ", e)

            # set old_points to the points of the new schedule (error occured because of a large difference)
            old_points = schedule.eval_schedule()

        list_of_points.append(old_points)
                       
        # increase the counter
        counter += 1

        # adjust the temperature
        temperature = start_temperature - ((start_temperature / repeats) * counter)

    # plot the malus points
    visualize_annealing(list_of_points)
    print("annealing_lessons_plot.png created in folder output_data")


    return schedule
 

