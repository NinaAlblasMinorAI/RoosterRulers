from code.classes import room
from code.classes.lesson import Lesson
from code.classes.room import Room
from code.classes.schedule import Schedule
import random

def place_lessons(schedule, lessons, algorithm):
    """
    Adds all lessons of a course to the schedule
    according to specified algorithm.
    """

    if algorithm == "randomize":
        randomize(schedule, lessons)


def randomize(schedule, lessons):
    """
    Randomly place lessons, disregarding room capacity.
    """

    # randomly shuffle lessons
    random.shuffle(lessons)
    
    # obtain room objects
    rooms = schedule.get_rooms()
    
    # obtain list of empty slot coordinates
    empty_slots = schedule.get_empty_slots()
    random.shuffle(empty_slots)

    for lesson in lessons:  

        slot = empty_slots.pop()

        # add the room to the lesson
        room_loc = slot[1]
        lesson.set_room(rooms[room_loc])
                
        # add the course to the schedule
        time_slot = slot[0]
        lesson.set_slot(time_slot + 1)
        schedule.place_lesson(lesson, (time_slot, room_loc))
    