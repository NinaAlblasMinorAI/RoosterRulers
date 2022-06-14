from code.classes.lesson import Lesson
from code.classes.room import Room
from code.classes.schedule import Schedule

def place_lesson(schedule, lessons):
    """
    Adds all lessons of a course to the schedule.
    """
    rooms = schedule.get_rooms()
    
    for lesson in lessons:  
        room_loc = 0
        time_slot = 0

        # get the number of students in the course
        number_of_students = lesson.get_nr_students()

        # if the course does not fit in the room, or the room is filled, 
        # or conflict with another lesson, go to the next one
        while number_of_students > rooms[room_loc].get_capacity() or schedule.get_dataframe().iloc[time_slot,room_loc] != 0:
        # while number_of_students > rooms[x].get_capacity() or schedule.iloc[y,x] != 0:
            room_loc += 1
    
            # after the last room, go to the next time slot
            if room_loc == 7:
                time_slot += 1
                room_loc = 0
            
            
        
        # add the room to the lesson
        lesson.set_room(rooms[room_loc])
                
        # add the course to the schedule
        lesson.set_slot(time_slot + 1)
        schedule.place_lesson(lesson, (time_slot, room_loc))
    