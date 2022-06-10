"""
loader.py

Minor programmeren
Programmeer Theorie

Helper functions to initialize all course and room objects from csv.
"""

import csv
from classes.room import Room
from classes.course import Course
from classes.student import Student


def init_rooms(filename):
    """
     Initializes all rooms of the schedule.
    """

    # declare a list to store room objects in
    rooms = []

    # open room data from csv
    with open(filename, "r") as file:
        csvreader = csv.reader(file)

        # skip header
        next(csvreader)
        for row in csvreader:

            # obtain arguments for room initializer
            id = row[0]
            capacity = int(row[1])

            # initialize room and add to list
            room = Room(id, capacity)
            rooms.append(room)
    
    return rooms


def init_students(filename):
    """
     Initializes all students in the schedule.
    """

    # declare a list to store room objects in
    students = []

    # open room data from csv
    with open(filename, "r") as file:
        csvreader = csv.reader(file)

        # skip header
        next(csvreader)
        for row in csvreader:

            # obtain arguments for room initializer
            name = row[1] + " " + row[0]
            number = int(row[2])
            course_names = []
            for i in range(3, 8):
                if row[i] != "":
                    course_names.append(row[i])

            # initialize room and add to list
            student = Student(name, number, course_names)
            students.append(student)
    
    return students


def init_courses(filename, students):
    """
     Initializes all courses to be put in the schedule.
    """

    # declare a list to store course objects in
    courses = []

    # open room data from csv
    with open(filename, "r") as file:
        csvreader = csv.reader(file)

        # skip header
        next(csvreader)
        for row in csvreader:

            # obtain arguments for course intitializer
            name = row[0]
            nr_lect = int(row[1])

            nr_tuto = int(row[2])
            if nr_tuto == 0: 
                max_students_tuto = 0
            else:
                max_students_tuto = int(row[3])

            nr_lab = int(row[4])
            if nr_lab == 0:
                max_students_lab = 0
            else:
                max_students_lab = int(row[5])

            E_students = int(row[6])

            # initialize course and add to list
            course = Course(name, E_students, nr_lect, nr_tuto, 
                            max_students_tuto, nr_lab, max_students_lab)
            courses.append(course)

            for student in students:
                for course_name in student._courses:
                    if course_name == course._name:
                        course.add_student(student)
    
    return courses

