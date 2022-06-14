from create_empty_schedule import build_empty_schedule
from loader import init_students, init_courses
from algorithms.create_lessons import create_lessons


def place_lesson(schedule, rooms, course_lessons):
    """Adds a course to the schedule"""
    forbidden_lectures = []
    forbidden_tutorials = []

    for lesson in course_lessons:  
        x = 0
        y = 0  
        # get the number of students in the course
        number_of_students = lesson._nr_students

        # if the course does not fit in the room, or the room is filled, go to the next one
        while number_of_students > rooms[x].get_capacity() or schedule.iloc[y,x] != 0 or y in forbidden_lectures:
        # while number_of_students > rooms[x].get_capacity() or schedule.iloc[y,x] != 0:
            x += 1
    
            # after the last room, go to the next time slot
            if x == 7:
                y += 1
                x = 0
            
            if lesson._type == "lab":
                while y in forbidden_tutorials:
                    y += 1

            if y == 25:
                return "error"
        
        # add the room to the lesson
        lesson._room = rooms[x]
        if lesson._type == "lecture":
            forbidden_lectures.append(y)
        if lesson._type == "tutorial":
            forbidden_tutorials.append(y)
        

        # add the course to the schedule
        schedule.iloc[y,x]= lesson
        lesson._slot = y + 1

    # return the changed schedule
    return schedule