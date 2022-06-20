import random


def redistribute_courses(schedule, algorithm):
    """
    redistributes courses into lessons
    according to specified algorithm.
    """

    if algorithm == "hillclimber":
        new_schedule = hillclimber(schedule)

    return new_schedule


def hillclimber(schedule):
    """
    Applies the hillclimber algorithm to a schedule.
    """

    # hillclimber stops when the number of malus points does not decrease after <threshold> times
    threshold = 200
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