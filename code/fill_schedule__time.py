from empty_schedule import build_empty_schedule
from loader import init_students, init_courses
from create_lessons import create_lessons
from place_course import place_course

# import the empty schedule
schedule = build_empty_schedule()

# get a list of courses
students = init_students("../data/students.csv")
courses = init_courses("../data/courses.csv", students)

# get a list of rooms from the headers of the schedule
rooms = schedule.columns.values.tolist()

# get the lessons from the courses
lessons = create_lessons(courses)

# place the lessons in the schedule
for lesson in lessons:
    place_course(schedule, rooms, lesson)
    
print(schedule)
schedule.to_csv("../data/schedule_time.csv")