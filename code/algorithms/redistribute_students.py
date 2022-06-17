import math
import random


def redistribute_students(schedule, algorithm):
    """
    Adds all lessons of a course to the schedule
    according to specified algorithm.
    """

    if algorithm == "hillclimber":
        new_schedule = hillclimber(schedule)
    # elif algorithm == "restart hillclimber":
    #     new_schedule = restart_hillclimber(schedule)

    return new_schedule

def hillclimber(schedule):
    """
    Take a schedule and apply
    the hillclimber algorithm to swapping of students.
    """

    # variables to keep track of malus points of old and new schedule
    outer_old_points = schedule.eval_schedule()
    outer_new_points = 0

    # hillclimber stops when the number of malus points does not decrease after <threshold> times
    outer_threshold = 500
    outer_counter = 0

    timeslot_list = list(schedule.get_timeslots().values())

    while outer_counter != outer_threshold:

        # get random tutorial or lab in schedule
        while True:
            random_loc = random.choice(timeslot_list)
            lesson = schedule.get_cell_content(random_loc)
            if lesson != 0:
                type = lesson.get_type()
                if type != "lecture":
                    break
        
        # get other lessons of the same type and randomly pick one
        group_nr = lesson.get_group_nr()
        others = [lesson for lesson in schedule.get_lessons() if lesson.get_type() == type and lesson.get_group_nr() != group_nr]
        other_lesson = random.choice(others)

        # randomly swap students based on hillclimber algorithm
        inner_old_points = outer_old_points
        inner_new_points = 0

        inner_threshold = 50
        inner_counter = 0
        
        while inner_counter != inner_threshold:
            index_student1 = random.randint(0, lesson.get_max_nr_students() - 1)
            index_student2 = random.randint(0, other_lesson.get_max_nr_students() - 1)

            if index_student1 + 1 > lesson.get_nr_students():
                student1 = None
            else:
                student1 = lesson.get_students()[index_student1]

            if index_student2 + 1 > other_lesson.get_nr_students():
                student2 = None
            else:
                student2 = other_lesson.get_students()[index_student2]

            schedule.swap_students(student1, lesson, student2, other_lesson)

            # obtain malus points of new schedule
            inner_new_points = schedule.eval_schedule()

            print(f"New points: {inner_new_points}  |  Lowest points: {inner_old_points}")

            if inner_new_points >= inner_old_points:
                schedule.swap_students(student1, other_lesson, student2, lesson)
                inner_counter += 1
            else:
                inner_old_points = inner_new_points
                inner_counter = 0

        outer_new_points = schedule.eval_schedule()

        if outer_new_points >= outer_old_points:
            outer_counter += 1
        else:
            outer_old_points = outer_new_points
            outer_counter = 0

    return schedule