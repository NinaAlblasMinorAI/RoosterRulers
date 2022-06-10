from classes.lesson import Lesson
import math

def create_lessons(courses):

    # create an empty list of lessons
    lessons = []
    for course in courses:
        # create the lectures based on the number of lectures in the course
        for i in range(course._nr_lect):
            # index the lectures, because there may be multiple per course
            lesson_name = f"{course._name}({i + 1})"

            # set the number of students in the lesson to the number of students in the course
            lesson_nr_students = len(course._students)
            
            lesson_type = "lecture"

            # create the lesson
            lesson = Lesson(lesson_name, lesson_nr_students, lesson_type)

            # fill the lesson with all the students from the course
            lesson._students = course._students

            # append the lesson to the list of lessons
            lessons.append(lesson)

        # create the tutorials
        if course._nr_tuto == 1:
            # calculate the number of lessons
            number_of_lessons = math.ceil(len(course._students) / course._max_students_tuto)

            # calculate the students per lesson
            students_per_lesson = math.ceil(len(course._students) / number_of_lessons) 

            # copy the students from the course, so that they can be devided
            students = course._students.copy()

            # create the lessons
            for i in range(number_of_lessons):
                lesson_name = f"{course._name}({i + 1})"

                # set the number of students
                lesson_nr_students = students_per_lesson
                lesson_type = "tutorial"

                # create the lesson
                lesson = Lesson(lesson_name, lesson_nr_students, lesson_type)
                for j in range(lesson_nr_students):
                    if len(students) > 0:

                        # get a student from the list of students
                        student = students.pop()

                        # add the lesson to the student lessons
                        student._lessons.append(lesson)

                        # add the student to the lesson
                        lesson._students.append(student)

                # add the lesson to the list of lessons        
                lessons.append(lesson)

        # create the labs
        if course._nr_lab == 1:
            # calculate the number of lessons
            number_of_lessons = math.ceil(len(course._students) / course._max_students_lab) 

            # calculate the students per lesson
            students_per_lesson = math.ceil(len(course._students) / number_of_lessons) 

             # copy the students from the course, so that they can be devided
            students = course._students.copy()

            # create the lessons
            for i in range(number_of_lessons):
                lesson_name = f"{course._name}({i + 1})"

                # set the number of students
                lesson_nr_students = students_per_lesson
                lesson_type = "lab"

                 # create the lesson
                lesson = Lesson(lesson_name, lesson_nr_students, lesson_type)
                for j in range(lesson_nr_students):
                    if len(students) > 0:

                        # get a student from the list of students
                        student = students.pop()

                        # add the lesson to the student lessons
                        student._lessons.append(lesson)

                        # add the student to the lesson
                        lesson._students.append(student) 
                
                # add the lesson to the list of lessons 
                lessons.append(lesson)
    lessons.sort(key=lambda x: x._nr_students)
    return lessons