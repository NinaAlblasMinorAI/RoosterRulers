from code.classes import room
from code.classes.lesson import Lesson
from code.classes.room import Room
from code.classes.schedule import Schedule
from code.algorithms.move_to_empty_slot import move_to_empty_slot
from copy import deepcopy
import math
import random

def place_lessons(schedule, lessons, algorithm):
    """
    Adds all lessons of a course to the schedule
    according to specified algorithm.
    """

    if algorithm == "randomize":
        randomize(schedule, lessons)
    elif algorithm == "hillclimber":
        hillclimber(schedule, lessons)


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

def hillclimber(schedule, lessons):
    """
    Take a randomly generated schedule and applies
    the hillclimber algorithm to it.
    """
    # TODO: Dit is de normale hillclimber, wij willen mss de Restart Hill Climber (RHC)
    # (bij de RHC check je of de malus points bijv. 80 keer niet verbeterd zijn)

    thres = 10 ** -6 # good number?

    old_malus_points = math.inf
    new_malus_points = 0

    # obtain list of empty slot coordinates
    empty_slots = schedule.get_empty_slots()
    random.shuffle(empty_slots)

    # while not converged (no minimum reached)
    while (old_malus_points - new_malus_points) > thres:

        # store the old schedule
        old_schedule = schedule.deepcopy()

        # choose random lesson              -- of worden deze al ergens geshuffled?
        lesson = random.choice(lessons) 

        # TODO: niet eerst proberen naar een empty slot te moven, kies gewoon een random slot uit het schedule
        # en je hoeft niet te kijken of dit past (want strafpunten)
        # Dus die if-else hieronder moet vervangen worden door een algemenere versie waarin we gewoon naar EEN
        # andere slot moven, niet per se een lege.

        # if it's possible to move to an empty slot in the copy of the schedule
        if move_to_empty_slot(old_schedule, lesson, empty_slots):

            # apply adjustment on the real schedule
            schedule = move_to_empty_slot(schedule, lesson, empty_slots)

        else:

            # TODO: swap lesson with another lesson in the real (?) schedule


        # als de malus points van dit aangepaste rooster > oude malus points: zet terug naar oude rooster
        # anders: old_malus_points = new_malus_points, new_malus_points = current_malus_points