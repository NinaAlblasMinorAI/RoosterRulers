from code.classes.schedule import Schedule

# build emtpy schedule
room_file = ("input_data/rooms.csv")
student_file = ("input_data/students.csv")
course_file = ("input_data/courses.csv")
schedule = Schedule(room_file, student_file, course_file)

# fill schedule randomly
schedule.fill_schedule()

# compute malus points
malus_points = schedule.eval_schedule()
print(malus_points)