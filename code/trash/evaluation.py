
def compute_malus_points(students, lessons):
    """
    Computes the number of malus points 
    based on the individual schedules of the students and overall schedule.
    """
    
    # initialize all the points
    for lesson in lessons:
        lesson._points_conflicts = 0
        lesson._points_gaps = 0
        lesson._points_capacity = 0
        lesson._points_evening = 0
    
    malus_points = 0

    # calculate malus points for each student's individual schedule
    for student in students:

        # build personal schedule
        schedule = []

        # go over each registered lesson
        for lesson in student._lessons:

            # check day and time of lesson and add to slot
            slot = {}
            day = int(lesson._slot / 5)
            time = lesson._slot % 5
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
                    lesson = student._lessons[i]
                    if anker_time == comp_time:             # if course conflict, 1 malus point
                        lesson._points_conflicts += 1
                    elif abs(anker_time - comp_time) == 2:  # if 1 time slot in between, 1 malus point
                        lesson._points_gaps += 1
                    elif abs(anker_time - comp_time) == 3:  # if 2 time slots in between, 3 malus points
                        lesson._points_gaps += 3
                    elif abs(anker_time - comp_time) > 3:   # schedules with 3 time slots in between are not valid
                        print("invalid schedule")
                        return "Invalid Schedule"
    
    # calculate malus points for each lesson
    for lesson in lessons:

        # obtain room of lesson
        room = lesson._room

        # add malus points for students in lesson exceeding room capacity
        if len(lesson._students) > room._capacity:
            excess = len(lesson._students) - room._capacity
            lesson._points_capacity += excess
        
        # add malus points if evening slot is used
        if room._id == "C0.110":
            time = lesson._slot % 5
            if time == 0:
                lesson._points_evening += 5
        
        malus_points += lesson.total_malus_points()
        
    return malus_points, lessons
