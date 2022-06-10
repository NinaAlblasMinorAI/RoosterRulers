from fill_schedule import fill_schedule
from create_empty_schedule import build_empty_schedule
from evaluation import compute_malus_points

# import the empty schedule
schedule = build_empty_schedule()

schedule_students = fill_schedule(schedule)
schedule = schedule_students[0]
lessons = schedule_students[1]
students = schedule_students[2]

malus_points = compute_malus_points(students, lessons)

print(malus_points[0])

for lesson in malus_points[1]:
    print(lesson.total_malus_points())