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

def get_empty_slots(schedule):
    empty_slots = []
    x = 0
    y = 0
    for x in range(7):
        for y in range(25):
            if schedule.iloc[y,x] == 0:
                
                empty_slots.append((y,x))
        
    
       
    return empty_slots
