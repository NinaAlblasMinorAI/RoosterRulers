from code.classes.lesson import Lesson


def course_greedy(schedule):
    """
    Takes the four lessons (labs or tutorials) with the most malus points
    and divides them into two lessons each.
    """

    # get list of lessons that have malus points
    schedule.eval_schedule_objects()
    lessons = [lesson for lesson in schedule.get_lessons() if lesson.get_malus_points() > 0 and lesson.get_type() != "lecture"]

    # sort the list of lessons based on number of malus points and get the four with the most
    lessons.sort(key=lambda x: x.get_malus_points(), reverse=True)
    worst_lessons = lessons[0:8]

    empty_slots = schedule.get_empty_slots()

    for lesson in worst_lessons:
        
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

        # place new lesson in empty slot in schedule
        random_loc = empty_slots.pop()
        schedule.place_content(new_lesson, random_loc)

    return schedule