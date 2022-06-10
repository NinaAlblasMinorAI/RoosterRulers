from fill_schedule import fill_schedule
from create_empty_schedule import build_empty_schedule
from evaluation import individual_course_registration, lesson_division

# import the empty schedule
schedule = build_empty_schedule()

schedule_students = fill_schedule(schedule)
schedule = schedule_students[0]
lessons = schedule_students[1]
students = schedule_students[2]

malus_points_students = individual_course_registration(students)
# malus_points_schedule = lesson_division(lessons)

# malus_points = malus_points_students + malus_points_schedule

print(malus_points_students)