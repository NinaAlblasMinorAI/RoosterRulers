from classes.lesson import Lesson
import math


def create_lessons(course):
        """
        Create lesson objects of the course.
        Returns lessons as list.
        """

        # # sort courses based on number of students
        # self._courses.sort(key=lambda x: x._E_students, reverse=True)

        lessons = []

        # create the lectures
        lectures = create_lectures(course)
        lessons.extend(lectures)

        # create the tutorials
        if course.has_nr_lessons("tutorial") == 1:
            tutorials = create_tutos_and_labs(course, "tutorial")
            lessons.extend(tutorials)

        # create the labs
        if course.has_nr_lessons("lab") == 1:
            labs = create_tutos_and_labs(course, "lab")
            lessons.extend(labs)
        
        return lessons


def create_lectures(course):
    """
    Creates the lecture lessons for a course.
    """

    lessons = []
    for i in range(course.has_nr_lessons("lecture")):

        # create name of lesson and set nr students equal to students in course
        lesson_name = f"{course.has_name()}({i + 1})"
        lesson_nr_students = len(course.has_students())
        lesson_type = "lecture"

        # create the lesson
        lesson = Lesson(lesson_name, lesson_nr_students, lesson_type)

        # associate the lesson with students
        students = course.has_students()
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
    students = list(course.has_students()).copy()

    # calculate the number of lessons and students per lesson
    number_of_lessons = math.ceil(len(students) / course.has_max_students(type))
    students_per_lesson = math.ceil(len(students) / number_of_lessons) 

    # create the lessons
    lessons = []
    for i in range(number_of_lessons):

        lesson_name = f"{course.has_name()}({i + 1})"
        lesson_nr_students = students_per_lesson
        lesson_type = type

        # create the lesson
        lesson = Lesson(lesson_name, lesson_nr_students, lesson_type)
        for j in range(lesson_nr_students):
            if len(students) > 0:

                # add lesson to student and student to lesson
                student = students.pop()
                student.add_lesson(lesson)
                lesson.add_student(student)
        
        # add the lesson to list
        lessons.append(lesson)

    return lessons