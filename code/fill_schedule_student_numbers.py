from empty_schedule import build_empty_schedule
from loader import init_students, init_courses
from algorithms.create_lessons import create_lessons
from algorithms.place_lesson import place_lesson

# import the empty schedule
schedule = build_empty_schedule()

# get a list of courses
students = init_students("../input_data/students.csv")
courses = init_courses("../input_data/courses.csv", students)

# get a list of rooms from the headers of the schedule
rooms = schedule.columns.values.tolist()

# get the lessons from the courses
lessons = create_lessons(courses)

# start with the lesson with the largest number of students
lessons.sort(key=lambda x: x._nr_students, reverse=True)

# place the lessons in the schedule
for lesson in lessons:
    place_lesson(schedule, rooms, lesson)

# print the schedule to the screen
print(schedule)

# write the schedule to the output_data folder
schedule.to_csv("../output_data/schedule_student_numbers.csv")