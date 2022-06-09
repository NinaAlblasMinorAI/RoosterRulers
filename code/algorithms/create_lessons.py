from classes.lesson import Lesson
import math

def create_lessons(courses):
    lessons = []
    for course in courses:
        # create the lectures
        for i in range(course._nr_lect):
            lesson_name = f"{course._name}({i + 1})"
            lesson_nr_students = course._E_students
            lesson_type = "lecture"
            lesson = Lesson(lesson_name, lesson_nr_students, lesson_type)
            lesson._students = course._students
            lessons.append(lesson)
        if course._nr_tuto == 1:
            number_of_lessons = math.ceil(course._E_students / course._max_students_tuto)
            students_per_lesson = math.ceil(course._E_students / number_of_lessons) 
            students = course._students.copy()
            for i in range(number_of_lessons):
                lesson_name = f"{course._name}({i + 1})"
                lesson_nr_students = students_per_lesson
                lesson_type = "tutorial"
                lesson = Lesson(lesson_name, lesson_nr_students, lesson_type)
                for j in range(lesson_nr_students):
                    if len(students) > 0:
                        student = students.pop()
                        student._lessons.append(lesson)
                        lesson._students.append(student)
                lessons.append(lesson)
        if course._nr_lab == 1:
            number_of_lessons = math.ceil(course._E_students / course._max_students_lab) 
            students_per_lesson = math.ceil(course._E_students / number_of_lessons) 
            students = course._students.copy()
            for i in range(number_of_lessons):
                lesson_name = f"{course._name}({i + 1})"
                lesson_nr_students = students_per_lesson
                lesson_type = "lab"
                lesson = Lesson(lesson_name, lesson_nr_students, lesson_type)
                for j in range(lesson_nr_students):
                    if len(students) > 0:
                        student = students.pop()
                        student._lessons.append(lesson)
                        lesson._students.append(student) 
                lessons.append(lesson)
    
    return lessons