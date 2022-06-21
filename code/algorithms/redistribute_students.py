import random
from code.visualization.visualize_hillclimber import visualize_hillclimber


def redistribute_students(schedule, algorithm):
    """
    Shuffles students between lessons of the same type
    according to specified algorithm.
    """

    if algorithm == "hillclimber":
        new_schedule = hillclimber(schedule)

    return new_schedule


def hillclimber(schedule):
    """
    Applies the hillclimber algorithm to a schedule.
    """

    # variables to keep track of malus points of old and new schedule
    outer_old_points = schedule.eval_schedule()
    outer_new_points = 0

    # keep track of the points in a list
    list_of_points = [outer_old_points]

    # hillclimber stops when the number of malus points does not decrease after <threshold> times
    outer_threshold = 2
    outer_counter = 0

    while outer_counter < outer_threshold:

        # get random tutorial or lab in schedule
        while True:
            random_loc = schedule.get_random_loc()
            lesson = schedule.get_cell_content(random_loc)
            if lesson != 0:
                type = lesson.get_type()
                if type != "lecture":
                    break
        
        # get other lessons of the same type and randomly pick one
        group_nr = lesson.get_group_nr()
        others = [
                    other_lesson for other_lesson in schedule.get_lessons() 
                    if other_lesson.get_name() == lesson.get_name() 
                    and other_lesson.get_type() == type 
                    and other_lesson.get_group_nr() != group_nr
                ]
        other_lesson = random.choice(others)

        # randomly swap students based on hillclimber algorithm
        inner_old_points = outer_old_points
        inner_new_points = 0

        inner_threshold = 50
        inner_counter = 0
        
        while inner_counter < inner_threshold:
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

            # print(f"New points: {inner_new_points}  |  Lowest points: {inner_old_points}")

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

    # plot the malus points
    visualize_hillclimber(list_of_points, finetune=True)
    print("redistribute_hillclimber_plot.png created in folder output_data")

    return schedule