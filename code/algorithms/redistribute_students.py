import random


def student_hillclimber(schedule, outer_repeats, inner_repeats, verbose):
    """
    Applies the hillclimber algorithm to a schedule.
    """

    # variables to keep track of malus points of old and new schedule
    outer_old_points = schedule.eval_schedule()
    outer_new_points = 0
    outer_counter = 0

    # keep track of the points in a list
    list_of_points = [outer_old_points]

    # hillclimber stops when the number of malus points does not decrease after <outer_repeat> times
    while outer_counter < outer_repeats:

        # get random tutorial or lab in schedule
        while True:
            random_loc = schedule.get_random_loc()
            random_lesson = schedule.get_cell_content(random_loc)
            if random_lesson != 0:
                type = random_lesson.get_type()
                if type != "lecture":
                    break
        
        # get other lessons of the same type and randomly pick one
        # group_nr = lesson.get_group_nr()
        all_lessons = [
                    lesson for lesson in schedule.get_lessons() 
                    if lesson.get_name() == random_lesson.get_name() 
                    and lesson.get_type() == type
                ]
        # other_lesson = random.choice(others)
        
        # randomly swap students based on hillclimber algorithm
        inner_old_points = outer_old_points
        inner_new_points = 0
        inner_counter = 0
        
        while inner_counter < inner_repeats:

            # randomly pick two different lessons
            lesson = None
            other_lesson = None
            while lesson == other_lesson:
                lesson = random.choice(all_lessons)
                other_lesson = random.choice(all_lessons)

            index_student1 = random.randint(0, lesson.get_max_students() - 1)
            index_student2 = random.randint(0, other_lesson.get_max_students() - 1)

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

            if verbose:
                print(f"Student hillclimber: New points: {inner_new_points}  |  Lowest points: {inner_old_points}")

            if inner_new_points > inner_old_points:
                schedule.swap_students(student1, other_lesson, student2, lesson)
                inner_counter += 1
            elif inner_new_points == inner_old_points:
                inner_counter += 1
            else:
                inner_old_points = inner_new_points
                inner_counter = 0

            list_of_points.append(inner_old_points)

        outer_new_points = schedule.eval_schedule()

        if outer_new_points >= outer_old_points:
            outer_counter += 1
        else:
            outer_old_points = outer_new_points
            outer_counter = 0

    return schedule, list_of_points