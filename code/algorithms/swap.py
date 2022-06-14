def swap_lesson(schedule, lesson, slot_swap):

    rooms = schedule.columns.values.tolist()

    slot = lesson._slot
    room = lesson._room._location

     
    # get the number of students in the course
    number_of_students = lesson._nr_students
    # if the course does not fit in the room, or the room is filled, go to the next one
    x = slot_swap[1]
    y = slot_swap[0]
    if number_of_students <= rooms[x].get_capacity():
        lesson._room = rooms[x]
        schedule.iloc[y,x]= lesson
        lesson._slot = y + 1
        schedule.iloc[slot - 1,room]= 0
    return schedule