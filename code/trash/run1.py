from fill_schedule import fill_schedule
from create_empty_schedule import build_empty_schedule
from evaluation import compute_malus_points
from algorithms.swap import swap_lesson, get_empty_slots

# import the empty schedule


for i in range(1):
    schedule = build_empty_schedule()
    schedule_students = fill_schedule(schedule)
    schedule = schedule_students[0]
    lessons = schedule_students[1]
    students = schedule_students[2]

    malus_points = compute_malus_points(students, lessons)
    malus_points[1].sort(key=lambda x: x.total_malus_points(), reverse=True)
    print(malus_points[0])

for i in range(10):
    
    empty_slots = get_empty_slots(schedule)

    best = 1000
    for slot in empty_slots:

        swap_lesson(schedule, malus_points[1][0], slot)
        # schedule.to_csv("../output_data/schedule_student_numbers_swap.csv")
        calculated_points = compute_malus_points(students, lessons)[0]
        if calculated_points < best:
            best = calculated_points
            best_slot = slot
            print(calculated_points)

    swap_lesson(schedule, malus_points[1][0], best_slot)
    malus_points = compute_malus_points(students, lessons)
    print(malus_points[0])
    
    malus_points[1].sort(key=lambda x: x.total_malus_points(), reverse=True)
    
# write the schedule to the output_data folder
schedule.to_csv("../output_data/schedule_student_numbers_swap.csv")

print(malus_points[0])

