def move_to_empty_slot(schedule, lesson, empty_slots):
    """
    Move the lesson to an empty slot in the schedule.
    Returns x if it was successful, otherwise y.
    """

    list_of_rooms = schedule._rooms

    # get the number of students in the course
    number_of_students = lesson._nr_students

    # loop over the list of empty slot tuples (x, y)
    for slot_index, slot in enumerate(empty_slots):

        # retrieve this slot's room capacity
        df_col_index = slot[0]
        room = list_of_rooms[df_col_index]
        room_capacity = room.get_capacity()

        # if the schedule is invalid or the lesson doesn't fit into the room, 
        # move lesson to next empty slot, else: store it
        if schedule.is_valid() and number_of_students <= room_capacity:

            # move lesson to empty slot
            lesson.set_room(room)
            time_slot = slot[0]
            lesson.set_slot(time_slot + 1)
            schedule.place_lesson(lesson, (slot[1], slot[0]))

            # remove coords from empty slots
            del empty_slots[slot_index]

            return schedule

    return False

# def swap_lesson(schedule, lesson, slot_swap):

#     rooms = schedule.columns.values.tolist()

#     slot = lesson._slot
#     room = lesson._room._location

     
#     # get the number of students in the course
#     number_of_students = lesson._nr_students
#     # if the course does not fit in the room, or the room is filled, go to the next one
#     x = slot_swap[1]
#     y = slot_swap[0]
#     if number_of_students <= rooms[x].get_capacity():
#         lesson._room = rooms[x]
#         schedule.iloc[y,x]= lesson
#         lesson._slot = y + 1
#         schedule.iloc[slot - 1,room]= 0
#     return schedule