from fill_schedule import fill_schedule
from create_empty_schedule import build_empty_schedule
from evaluation import individual_course_registration

# import the empty schedule
schedule = build_empty_schedule()

schedule_students = fill_schedule(schedule)
schedule = schedule_students[0]
students = schedule_students[1]

malus_points = individual_course_registration(students)

print(malus_points)