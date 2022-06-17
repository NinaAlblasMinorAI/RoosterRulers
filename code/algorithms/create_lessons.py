import random
from code.classes.lesson import Lesson
import math


def create_lessons(schedule):
    """
    Create lesson objects of the course.
    Returns lessons as list.
    """

    lessons = []

    courses = schedule.get_courses().values()
    for course in courses:

        # randomly shuffle the students in the course
        random.shuffle(course.get_students())

        # create the lectures
        lectures = create_lectures(course)
        lessons.extend(lectures)

        # create the tutorials
        if course.get_nr_lessons("tutorial") == 1:
            tutorials = create_tutos_and_labs(course, "tutorial")
            lessons.extend(tutorials)

        # create the labs
        if course.get_nr_lessons("lab") == 1:
            labs = create_tutos_and_labs(course, "lab")
            lessons.extend(labs)
    
    schedule.add_lessons(lessons)


def create_lectures(course):
    """
    Creates the lecture lessons for a course.
    """

    lessons = []
    for i in range(course.get_nr_lessons("lecture")):

        # create name of lesson and set nr students equal to students in course
        lesson_name = f"{course.get_name()}"
        lesson_type = "lecture"
        lesson_group_nr = i + 1
        max_nr_students = None
        
        # create the lesson
        lesson = Lesson(lesson_name, lesson_type, lesson_group_nr, max_nr_students)

        # associate the lesson with students
        students = course.get_students()
        for student in students:
            lesson.add_student(student)

        # append the lesson to list
        lessons.append(lesson)
    
    return lessons


def create_tutos_and_labs(course, type):
    """
    Creates the tutorial and lab lessons for a course.
    """

    # copy the students from the course, so that they can be devided
    students = list(course.get_students()).copy()

    # calculate the number of lessons and students per lesson
    max_students = course.get_max_students(type)
    number_of_lessons = math.ceil(len(students) / max_students)
    students_per_lesson = math.ceil(len(students) / number_of_lessons) 

    # create the lessons
    lessons = []
    for i in range(number_of_lessons):
        
        lesson_name = f"{course.get_name()}"
        lesson_type = type
        lesson_group_nr = i + 1
        
        # create the lesson
        lesson = Lesson(lesson_name, lesson_type, lesson_group_nr, max_students)

        for j in range(students_per_lesson):
            if len(students) > 0:

                # add lesson to student and student to lesson
                student = students.pop()
                student.add_lesson(lesson)
                lesson.add_student(student)
        
        # add the lesson to list
        lessons.append(lesson)

    return lessons