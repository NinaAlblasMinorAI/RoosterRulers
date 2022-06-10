from create_empty_schedule import build_empty_schedule
from loader import init_students, init_courses
from algorithms.create_lessons import create_lessons
from algorithms.place_lesson import place_lesson

def fill_schedule(schedule):
    lessons = []
    
    # get a list of students and courses
    students = init_students("../input_data/students.csv")
    courses = init_courses("../input_data/courses.csv", students)

    # get a list of rooms from the headers of the schedule
    rooms = schedule.columns.values.tolist()

    for course in courses:
        course_lessons = create_lessons([course])
        lessons.extend(course_lessons)
        # place the lessons in the schedule
        place_lesson(schedule, rooms, course_lessons)

    # start with the lesson with the largest number of students
    # lessons.sort(key=lambda x: x._nr_students, reverse=True)

    

    # print the schedule to the screen
    print(schedule)
    
    # write the schedule to the output_data folder
    schedule.to_csv("../output_data/schedule_student_numbers.csv")

    return (schedule, lessons, students)