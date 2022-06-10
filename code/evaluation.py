
def individual_course_registration(students):
    """
    Computes the number of malus points 
    based on the individual schedules of the students.
    """

    malus_points = 0

    # calculate malus points for each student
    for student in students:

        # build personal schedule
        schedule = []

        # go over each registered lesson
        for lesson in student._lessons:

            # create a time slot for each lesson
            slot = {}
            room = lesson._room

            # only the largest room has a fifth time slot
            if room == "C0.110":
                day = int(lesson._slot / 5)
                time = lesson._slot % 5
            else:
                day = int(lesson._slot / 4)
                time = lesson._slot % 4

            # add day and time of lesson to slot
            slot["day"] = day
            slot["time"] = time
            schedule.append(slot)
        
        # check the time between every combination of lessons
        for i in range(len(schedule)):
            anker_day = schedule[i]["day"] 
            anker_time = schedule[i]["time"]

            for j in range(i+1, len(schedule)):
                comp_day = schedule[j]["day"]
                comp_time = schedule[j]["time"]

                # only count malus points if lessons are given on the same day
                if anker_day == comp_day:
                    if anker_time == comp_time:             # if course conflict, 1 malus point
                        malus_points += 1
                    elif abs(anker_time - comp_time) == 2:  # if 1 time slot in between, 1 malus point
                        malus_points += 1
                    elif abs(anker_time - comp_time) == 3:  # if 2 time slots in between, 3 malus points
                        malus_points += 3
                    elif abs(anker_time - comp_time) > 3:   # schedules with 3 time slots in between are not valid
                        return "Invalid Schedule"
    
    return malus_points


def lesson_division(lessons):
    """
    Computes the number of malus points 
    based on the way lessons are divided over the schedule.
    """

    pass