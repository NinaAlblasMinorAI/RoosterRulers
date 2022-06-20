import random


def redistribute_courses(schedule, algorithm):
    """
    redistributes courses into lessons
    according to specified algorithm.
    """

    if algorithm == "greedy":
        new_schedule = greedy(schedule)

    return new_schedule


def greedy(schedule):
    """
    Applies the greedy algorithm to a schedule.
    """

    # get list of lessons that have malus points
    schedule.eval_schedule_elements()
    lessons = [lesson for lesson in schedule if lesson.get_malus_points() > 0 and lesson.get_type() != "lecture"]

    empty_slots = schedule.get_empty_slots()

    for lesson in lessons:

        # create lesson attributes
        lesson_name = lesson.get_name()
        lesson_type = lesson.get_type()
        lesson_group_nr = i + 1
        max_nr_students = None
        
        # create the lesson
        lesson = Lesson(lesson_name, lesson_type, lesson_group_nr, max_nr_students)
        lectures.append(lesson)

        # associate the lesson with students
        students = course.get_students()
        for student in students:
            lesson.add_student(student)
        
        # get two random locations in the schedule
        random_loc1 = schedule.get_random_loc()
        random_loc2 = schedule.get_random_loc()

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