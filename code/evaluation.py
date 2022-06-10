from classes.student import Student
from classes.course import Course
from classes.lesson import Lesson
import loader

def main():

    # get a list of students and courses
    students = loader.init_students("../input_data/students.csv")
    courses = loader.init_courses("../input_data/courses.csv", students)
    individual_schedule_points(students)


def individual_schedule_points(students):

    for student in students:
        schedule = []
        for lesson in student._lessons:
            slot = {}
            room = lesson._room
            if room._id == "C0.110":
                day = lesson._slot / 5
                time = lesson._slot % 5
            else:
                day = lesson._slot / 4
                time = lesson._slot % 4
            slot["day"] = day
            slot["time"] = time
            schedule.append(slot)
        
        print(schedule)
        for i in range(len(schedule)):
            for j in range(i+1, len(schedule)):
                print(i)
                print(j)

main()