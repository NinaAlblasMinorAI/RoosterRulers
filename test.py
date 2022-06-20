from code.classes.schedule import Schedule

# create a random schedule
random_schedule = Schedule()

lessons = random_schedule.get_lessons()
result_file = open(f"output_data/result.csv", "w")
result_file.write("student,course,activity,room,day,time\n")
for lesson in lessons:
    students = lesson.get_students()
    for student in students:
        result_string = f"{student._name},{lesson}\n"
        result_file.write(result_string)

result_file.close()