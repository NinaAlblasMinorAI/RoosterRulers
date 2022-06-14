from code.algorithms.create_lessons import create_lessons
<<<<<<< HEAD
from code.algorithms.place_lessons import place_lessons
=======
from algorithms.place_lessons import place_lessons
>>>>>>> e00efcee5da16677e80622cb6880751200cc4304
from code.classes.schedule import Schedule
import random

# build emtpy schedule
room_file = ("input_data/rooms.csv")
student_file = ("input_data/students.csv")
course_file = ("input_data/courses.csv")
schedule = Schedule(room_file, student_file, course_file)

# fill schedule randomly
lessons = create_lessons(schedule.get_courses())
schedule.add_lessons(lessons)
<<<<<<< HEAD
=======


random.shuffle(lessons)
>>>>>>> e00efcee5da16677e80622cb6880751200cc4304
place_lessons(schedule, lessons)

# compute malus points
malus_points = schedule.eval_schedule()
print(malus_points)

# visualize schedule
# visualize_schedule(schedule)