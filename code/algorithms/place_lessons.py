from copy import deepcopy
import math
import random


def place_lessons(schedule, algorithm):
    """
    Adds all lessons of a course to the schedule
    according to specified algorithm.
    """

    if algorithm == "randomize":
        randomize(schedule)
    elif algorithm == "hillclimber":
        hillclimber(schedule)


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


def hillclimber(schedule):
    """
    Take a randomly generated schedule and applies
    the hillclimber algorithm to it.
    """

    # TODO: Dit is de normale hillclimber, wij willen mss de Restart Hill Climber (RHC)
    # (bij de RHC check je of de malus points bijv. 80 keer niet verbeterd zijn)

    # hillclimber stops when the number of malus points does not decrease after <threshold> times
    threshold = 1000
    counter = 0

    # variables to keep track of malus points of old and new schedule
    old_points = math.inf
    new_points = 0

    timeslot_list = list(schedule.get_timeslots().values())

    while counter != threshold:

        # store the old schedule
        # old_schedule = deepcopy(schedule)

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

        if new_points >= old_points:
            # schedule = old_schedule
            schedule.swap_contents(random_loc2, random_loc1)
            counter += 1
        else:
            old_points = new_points
            counter = 0

        print(old_points)
