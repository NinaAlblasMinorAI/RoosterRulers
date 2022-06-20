import random

from code.classes.lesson import Lesson


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
        
        # get corresponding course object of lesson
        course = lesson.get_course()

        # create lesson attributes
        lesson_name = lesson.get_name()
        lesson_type = lesson.get_type()
        lesson_group_nr = course.get_nr_groups(lesson_type) + 1
        max_nr_students = lesson.get_max_students()
        
        # create the lesson
        new_lesson = Lesson(lesson_name, lesson_type, lesson_group_nr, max_nr_students, course)
        schedule.add_lesson(new_lesson)
        course.add_group(lesson_type)

        # transfer half of students to new lesson
        all_students = lesson.get_students()
        students = all_students[:int(len(all_students)/2)]
        for student in students:

            # remove student from old lesson and old lesson from student
            lesson.remove_student(student)
            student.remove_lesson(lesson)

            # add student to new lesson and new lesson to student
            new_lesson.add_student(student)
            student.add_lesson(new_lesson)



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

    # visualize greedy in plot?

    return schedule