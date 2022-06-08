from empty_schedule import build_empty_schedule
from loader import init_students, init_courses
from algorithms.create_lessons import create_lessons


def place_course(schedule, rooms, lesson):
    """Adds a course to the schedule"""
    x = 0
    y = 0
    
    # get the number of students in the course
    number_of_students = lesson._nr_students

    # if the course does not fit in the room, or the room is filled, go to the next one
    while number_of_students > rooms[x].get_capacity() or schedule.iloc[y,x] != 0:
        x += 1

        # after the last room, go to the next time slot
        if x == 7:
            y += 1
            x = 0
    
    # add the course to the schedule
    schedule.iloc[y,x]= lesson
    return schedule