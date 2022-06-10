from classes.student import Student
from classes.course import Course
from classes.lesson import Lesson
from empty_schedule import build_empty_schedule
from algorithms.create_lessons import create_lessons
from algorithms.place_lesson import place_lesson
import loader


def main():

    # import the empty schedule
    schedule = build_empty_schedule()

    # get a list of students and courses
    students = loader.init_students("../input_data/students.csv")
    courses = loader.init_courses("../input_data/courses.csv", students)

    # get a list of rooms from the headers of the schedule
    rooms = schedule.columns.values.tolist()

    # get the lessons from the courses
    lessons = create_lessons(courses)

    # place the lessons in the schedule
    for lesson in lessons:
        place_lesson(schedule, rooms, lesson)
    
    malus_points = individual_schedule_points(students)
    print(malus_points)


def individual_schedule_points(students):

    malus_points = 0

    for student in students:
        schedule = []
        for lesson in student._lessons:
            slot = {}
            room = lesson._room
            if room == "C0.110":
                day = int(lesson._slot / 5)
                time = lesson._slot % 5
            else:
                day = int(lesson._slot / 4)
                time = lesson._slot % 4
            slot["day"] = day
            slot["time"] = time
            schedule.append(slot)
        
        for i in range(len(schedule)):
            anker_day = schedule[i]["day"] 
            anker_time = schedule[i]["time"]

            for j in range(i+1, len(schedule)):
                comp_day = schedule[j]["day"]
                comp_time = schedule[j]["time"]

                print(anker_day, comp_day)
                print(anker_time, comp_time)
                if anker_day == comp_day:
                    if anker_time == comp_time:
                        malus_points += 1
                    elif abs(anker_time - comp_time) == 2:
                        malus_points += 1
                    elif abs(anker_time - comp_time) == 3:
                        malus_points += 3
                    elif abs(anker_time - comp_time) > 3:
                        return "Invalid Schedule"
    
    return malus_points


main()