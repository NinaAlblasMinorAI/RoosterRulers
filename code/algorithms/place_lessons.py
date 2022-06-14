from classes.lesson import Lesson
from classes.room import Room


def place_lesson(schedule, rooms, lessons):
    """
    Adds all lessons of a course to the schedule.
    """
    
    forbidden_y_lectures = []
    forbidden_y_tutorials = []

    for lesson in lessons:  
        x = 0
        y = 0

        # get the number of students in the course
        number_of_students = lesson.has_nr_students()

        # if the course does not fit in the room, or the room is filled, 
        # or conflict with another lesson, go to the next one
        while number_of_students > rooms[x].get_capacity() or schedule.iloc[y,x] != 0 or y in forbidden_y_lectures:
        # while number_of_students > rooms[x].get_capacity() or schedule.iloc[y,x] != 0:
            x += 1
    
            # after the last room, go to the next time slot
            if x == 7:
                y += 1
                x = 0
            
            if lesson.is_type() == "lab":
                while y in forbidden_y_tutorials:
                    y += 1

            if y == 25:
                return "error"
        
        # add the room to the lesson
        lesson.add_room(rooms[x])
        if lesson.is_type() == "lecture":
            forbidden_y_lectures.append(y)
        if lesson.is_type() == "tutorial":
            forbidden_y_tutorials.append(y)
        
        # add the course to the schedule
        lesson.set_slot(y + 1)
        schedule.place_lesson(lesson, (y, x))
    
    # return the changed schedule
    return schedule