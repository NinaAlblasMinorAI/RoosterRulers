from code.algorithms.create_lessons import create_lessons
from code.algorithms.place_lessons import place_lesson
from code.classes.schedule import Schedule

# build emtpy schedule
room_file = ("input_data/rooms.csv")
student_file = ("input_data/students.csv")
course_file = ("input_data/courses.csv")
schedule = Schedule(room_file, student_file, course_file)

# fill schedule randomly
lessons = create_lessons(schedule.get_courses())
schedule.add_lessons(lessons)
place_lesson(schedule, lessons)

# compute malus points
malus_points = schedule.eval_schedule()
print(malus_points)

# visualize schedule
# visualize_schedule(schedule)