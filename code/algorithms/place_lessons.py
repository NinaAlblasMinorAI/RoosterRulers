from copy import deepcopy
import math
import random


def place_lessons(schedule, algorithm):
    """
    Adds all lessons of a course to the schedule
    according to specified algorithm.
    """

    if algorithm == "randomize":
        new_schedule = randomize(schedule)
    elif algorithm == "hillclimber":
        new_schedule = hillclimber(schedule)
    elif algorithm == "restart_hillclimber":
        new_schedule = restart_hillclimber(schedule)
    elif algorithm == "simulated_annealing":
        new_schedule = simulated_annealing(schedule)

    return new_schedule


def randomize(schedule):
    """
    Randomly place lessons, disregarding room capacity.
    """

    # randomly shuffle lessons
    lessons = schedule.get_lessons()
    random.shuffle(lessons)
    
    # get random list of empty slot coordinates
    empty_slots = schedule.get_empty_slots()
    random.shuffle(empty_slots)

    for lesson in lessons:
        random_loc = empty_slots.pop()
        schedule.place_lesson(lesson, random_loc)

    return schedule


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

    timeslot_list = list(schedule.get_timeslots().values())

    while counter != threshold:

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

        print(f"New points: {new_points}  |  Lowest points: {old_points}")

        if new_points >= old_points:
            schedule.swap_contents(random_loc2, random_loc1)
            counter += 1
        else:
            old_points = new_points
            counter = 0

    return schedule

def restart_hillclimber(schedules):

    best_values = []
    for schedule in schedules:
        best_schedule = hillclimber(schedule)
        malus_points = best_schedule.eval_schedule()
        best_values.append(malus_points)

    min_value = min(best_values)
    min_index = best_values.index(min_value)

    return schedules[min_index]

def simulated_annealing(schedule):
    """
    Take a randomly generated schedule and applies
    the simulated annealing algorithm to it.
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

    # get the list of timeslots
    timeslot_list = list(schedule.get_timeslots().values())

    # run as long as the repeats are not reached, and the temperature is above 0.01 (to avoid dumps)
    while counter < repeats and temperature > 0.01:
    
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

        # print the new and old points
        print(f"New points: {new_points}  |  Lowest points: {old_points}")

        # get a random number between 0 and 1
        random_number = random.random()

        # calculate the change based on the old points, new points and temperature
        chance = 2 ** ((old_points - new_points) / temperature)

        # print the counter and temperature
        # print(f"counter: {counter}, temperature: {temperature}, random_number: {random_number}, chance: {chance}")
        print(f"counter: {counter}, temperature: {temperature}")

        # if the random number is higher than the chance, reverse the swap, else set the new point total
        if random_number > chance:
            schedule.swap_contents(random_loc2, random_loc1)
        else:
            old_points = new_points
            
        # increase the counter
        counter += 1

        # adjust the temperature
        temperature = start_temperature - ((start_temperature / repeats) * counter)
            
    return schedule
 

