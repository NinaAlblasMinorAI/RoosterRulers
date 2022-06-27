import csv
import math
import random
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN

from code.classes.room import Room
from code.classes.student import Student
from code.classes.course import Course
from code.classes.lesson import Lesson


class Schedule:

    def __init__(self):
        """
        Schedule object that contains the to be visualized dataframe.
        """

        # load in all room, student, and course objects
        self._rooms = self.load_rooms("input_data/rooms.csv")
        self._students = self.load_students("input_data/students.csv")
        self._courses = self.load_courses("input_data/courses.csv")

        # add students to each course
        self.add_students_to_courses()

        # create empty schedule and its time slots
        self._dataframe = self.build_empty_schedule()
        self._timeslots = self.create_timeslots()

        # create and place lessons
        self._lessons = self.create_lessons()
        self.place_lessons_randomly()


    def load_rooms(self, source_file):
        """
        Loads in all rooms of the schedule.
        """

        rooms = []
        with open(source_file, "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                room = Room(row['\ufeffZaalnummer'], int(row['Max. capaciteit']))
                rooms.append(room)

        # sort rooms based on capacity
        rooms.sort(key=lambda x: x._capacity)
        
        return rooms

    def load_students(self, source_file):
        """
        Loads in all students to fit in the schedule.
        """

        students = {}
        with open(source_file, "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                name = row["Voornaam"] + " " + row["Achternaam"]

                # build list of course names
                courses = []
                for i in range(1,6):
                    if row[f"Vak{i}"] != "":
                        courses.append(row[f"Vak{i}"])

                students[row['Stud.Nr.']] = Student(name, row['Stud.Nr.'], courses)
        
        return students

    def load_courses(self, source_file):
        """
        Initializes all courses to be put in the schedule.
        """

        courses = {}
        with open(source_file, "r") as file:
            reader = csv.DictReader(file)

            for row in reader:

                nr_tuto = int(row["#Werkcolleges"])
                if nr_tuto == 0: 
                    max_students_tuto = 0
                else:
                    max_students_tuto = int(row["Max. stud. Werkcollege"])

                nr_lab = int(row["#Practica"])
                if nr_lab == 0: 
                    max_students_lab = 0
                else:
                    max_students_lab = int(row["Max. stud. Practicum"])

                course = Course(row["Vak"], int(row["Verwacht"]), int(row["#Hoorcolleges"]), nr_tuto, 
                                max_students_tuto, nr_lab, max_students_lab)
                courses[row["Vak"]] = course

        return courses

    def add_students_to_courses(self):
        """
        Adds the registered students for each course.
        """

        for student in self._students.values():
            for course_name in student.get_courses():
                self._courses[course_name].add_student(student)

    def build_empty_schedule(self):
        """
        Builds the schedule without lessons associated to it.
        """

        # build list of all possible time slots (excluding evening slots)
        timeslots = ["Monday 09:00-11:00", "11:00-13:00", "13:00-15:00", "15:00-17:00",
                    "Tuesday 09:00-11:00", "11:00-13:00", "13:00-15:00", "15:00-17:00", 
                    "Wednesday 09:00-11:00", "11:00-13:00", "13:00-15:00", "15:00-17:00", 
                    "Thurday 09:00-11:00", "11:00-13:00", "13:00-15:00", "15:00-17:00", 
                    "Friday 09:00-11:00", "11:00-13:00", "13:00-15:00", "15:00-17:00", ]

        # build schedule without evening slots
        schedule = pd.DataFrame(index=timeslots, columns=self._rooms, data=0)
        
        # add the evening slots
        schedule = schedule.reset_index()

        for index in np.arange(3.5, 20.0, 4.0):
            schedule.loc[index] = ["17:00-19:00", "-", "-", "-", "-", "-", "-", 0]

        schedule = schedule.sort_index().reset_index(drop=True)
        schedule.set_index("index", inplace=True)
        schedule.index.names = ["Time"]

        return schedule

    def create_timeslots(self):
        """
        Create a dictionary of all timeslots.
        """
        
        timeslots = {}

        counter = 1
        for x in range(7):
            if x == 6:
                for y in range(25):
                    timeslots[counter] = (y, x)
                    counter += 1
            else:
                for y in range(25):
                    if (y + 1) % 5 == 0:
                        continue
                    timeslots[counter] = (y, x)
                    counter += 1

        return timeslots

    def create_lessons(self):
        """
        Create lesson objects of courses 
        with minimum number of lessons.
        """

        lessons = []
        for course in self._courses.values():

            # randomly shuffle the students in the course
            random.shuffle(course.get_students())

            # create the lectures
            lectures = self.create_lectures(course)
            lessons.extend(lectures)

            # create the tutorials
            if course.get_nr_lessons("tutorial") == 1:
                tutorials = self.create_tutos_and_labs(course, "tutorial")
                lessons.extend(tutorials)

            # create the labs
            if course.get_nr_lessons("lab") == 1:
                labs = self.create_tutos_and_labs(course, "lab")
                lessons.extend(labs)

        return lessons

    def create_lectures(self, course):
        """
        Creates the lecture lessons for a course.
        """

        # create the lessons
        lectures = []
        for i in range(course.get_nr_lessons("lecture")):

            # create lesson attributes
            lesson_name = course.get_name()
            lesson_type = "lecture"
            lesson_group_nr = i + 1
            max_nr_students = None
            
            # create the lesson
            lesson = Lesson(lesson_name, lesson_type, lesson_group_nr, max_nr_students, course)
            lectures.append(lesson)

            # associate the lesson with students
            students = course.get_students()
            for student in students:
                lesson.add_student(student)
                student.add_lesson(lesson)
        
        return lectures

    def create_tutos_and_labs(self, course, type):
        """
        Creates the tutorial or lab lessons for a course.
        """

        # copy the students from the course, so that they can be devided
        students = list(course.get_students()).copy()

        # calculate the number of lessons and students per lesson
        max_students = course.get_max_students(type)
        number_of_groups = math.ceil(len(students) / max_students)
        students_per_group = math.ceil(len(students) / number_of_groups) 

        # create the lessons
        lessons = []
        for i in range(number_of_groups):
            
            # create lesson attributes
            lesson_name = course.get_name()
            lesson_type = type
            lesson_group_nr = i + 1
            
            # create the lesson
            lesson = Lesson(lesson_name, lesson_type, lesson_group_nr, max_students, course)
            lessons.append(lesson)

            # add group counter to course
            course.add_group(type)
            
            for j in range(students_per_group):
                if len(students) > 0:

                    # add lesson to student and student to lesson
                    student = students.pop()
                    student.add_lesson(lesson)
                    lesson.add_student(student)

        return lessons
    
    def add_lesson(self, lesson):
        """
        Adds a lesson to the schedule.
        """

        self._lessons.append(lesson)

    def place_lessons_randomly(self):
        """
        Randomly place lessons, disregarding room capacity.
        """

        # randomly shuffle lessons
        random.shuffle(self._lessons)
        
        # get random list of empty slot coordinates
        empty_slots = self.get_empty_slots()
        random.shuffle(empty_slots)

        for lesson in self._lessons:
            random_loc = empty_slots.pop()
            self.place_content(lesson, random_loc)
        
        self.eval_schedule()

    def place_content(self, lesson, loc):
        """
        Place lesson in specified "zaalslot".
        loc = (y, x)
        """

        # set time slot and add room to lesson if present
        if isinstance(lesson, Lesson):
            slot = loc[0]
            lesson.set_slot(slot)

            room = self._rooms[loc[1]]
            lesson.set_room(room)

        # place lesson in schedule
        self._dataframe.iloc[loc]= lesson

    def swap_contents(self, loc1, loc2):
        """
        Swaps the contents of two positions in the schedule.
        loc = (y, x)
        """

        # request contents of schedule for specified locations
        content1 = self.get_cell_content(loc1)
        content2 = self.get_cell_content(loc2)

        # swap contents
        self.place_content(content2, loc1)
        self.place_content(content1, loc2)

    def swap_students(self, student1, lesson1, student2, lesson2):
        """
        Swaps two students between lessons of same type.
        """

        if student1 is not None and student2 is not None:
            
            # remove students from lessons and lessons from students
            lesson1.remove_student(student1)
            lesson2.remove_student(student2)
            student1.remove_lesson(lesson1)
            student2.remove_lesson(lesson2)

            # add students to lessons and lessons to students in reverse order
            lesson1.add_student(student2)
            lesson2.add_student(student1)
            student1.add_lesson(lesson2)
            student2.add_lesson(lesson1)
        
        elif student1 is not None and student2 is None:

            # remove student from lesson and lesson from student
            lesson1.remove_student(student1)
            student1.remove_lesson(lesson1)

            # add student to lesson and lesson to student
            lesson2.add_student(student1)
            student1.add_lesson(lesson2)

        elif student2 is not None and student1 is None:

            # remove student from lesson and lesson from student
            lesson2.remove_student(student2)
            student2.remove_lesson(lesson2)

            # add student to lesson and lesson to student           
            lesson1.add_student(student2)
            student2.add_lesson(lesson1)

        else:
            pass

    # def eval_schedule(self):
    #     """
    #     Computes and returns the number of malus points based on the 
    #     whole schedule (does not assign malus points to individual lessons and students).
    #     """

    #     malus_points = 0

    #     # calculate malus points for each student's individual schedule
    #     for student in self._students.values():

    #         # build personal schedule
    #         schedule = []
    #         for lesson in student.get_lessons():

    #             # check day and time of lesson and add to slot
    #             slot = {}
    #             slot["day"] = lesson.get_day()
    #             slot["time"] = lesson.get_time()
    #             schedule.append(slot)
            
    #         # check the time between every combination of lessons
    #         for i in range(len(schedule)):
    #             anker_day = schedule[i]["day"] 
    #             anker_time = schedule[i]["time"]

    #             for j in range(i+1, len(schedule)):
    #                 comp_day = schedule[j]["day"]
    #                 comp_time = schedule[j]["time"]

    #                 # only count malus points if lessons are given on the same day
    #                 if anker_day == comp_day:
    #                     lesson = student.get_lessons()[i]
    #                     if anker_time == comp_time:             # if course conflict, 1 malus point
    #                         malus_points += 1
    #                     elif abs(anker_time - comp_time) == 2:  # if 1 time slot in between, 1 malus point
    #                         malus_points += 1
    #                     elif abs(anker_time - comp_time) == 3:  # if 2 time slots in between, 3 malus points
    #                         malus_points += 3
    #                     elif abs(anker_time - comp_time) > 3:   # schedules with 3 time slots in between are not valid
    #                         malus_points += 100

    #     # calculate malus points for each lesson
    #     for lesson in self._lessons:
    #         room = lesson.get_room()

    #         # add malus points for students in lesson exceeding room capacity
    #         if len(lesson.get_students()) > room.get_capacity():
    #             excess = len(lesson.get_students()) - room.get_capacity()
    #             malus_points += excess
            
    #         # add malus points if evening slot is used
    #         if room.get_id() == "C0.110":
    #             time = lesson.get_time()
    #             if time == 0:
    #                 malus_points += 5
            
    #     return malus_points

    def eval_schedule(self):
        """
        Computes and returns the number of malus points based on the 
        whole schedule (does not assign malus points to individual lessons and students).
        """

        malus_points = 0

        # calculate malus points for each student's individual schedule
        for student in self._students.values():
            
            # create an empty dictionary of timeslots per day
            slots_per_day = {0:[],1:[],2:[],3:[],4:[]}
            
            # loop over all the lessons per student
            for lesson in student.get_lessons():
                
                # check day and time of lesson and add the timeslot to the correct day
                day = lesson.get_day()
                time = lesson.get_time()
                slots_per_day[day].append(time) 
                        
            # count the malus points for lessons on the same day
            for timeslots in slots_per_day.values():
                
                if len(timeslots) > 0:

                    # sort the timeslots
                    timeslots.sort()
                                    
                    # calculate the gaps in the timeslots
                    # https://stackoverflow.com/questions/16974047/efficient-way-to-find-missing-elements-in-an-integer-sequence
                    start, end = timeslots[0], timeslots[-1]
                    gaps = sorted(set(range(start, end + 1)).difference(timeslots))  
                    number_of_gaps = len(gaps)
                    
                    # assign 100 malus point for 3 gaps to the student and lesson
                    if number_of_gaps == 3:
                        number_of_gaps = 100
                        # print(timeslots)

                    # assign 3 malus points for 2 adjacent gaps
                    if number_of_gaps == 2 and gaps !=  [0, 2, 4]:
                        number_of_gaps = 3

                    # otherwise, assign malus point per gap
                    malus_points += number_of_gaps
                    
                # if timeslots exist multiple times, assign malus points for conflicts   
                if len(timeslots) > len(set(timeslots)):
                    conflicts = len(timeslots) - len(set(timeslots))
                    malus_points += conflicts
                     
        # calculate malus points for each lesson
        for lesson in self._lessons:
            room = lesson.get_room()

            # add malus points for students in lesson exceeding room capacity
            if len(lesson.get_students()) > room.get_capacity():
                excess = len(lesson.get_students()) - room.get_capacity()
                malus_points += excess
            
            # add malus points if evening slot is used
            if room.get_id() == "C0.110":
                time = lesson.get_time()
                if time == 4:
                    malus_points += 5
            
        return malus_points

    def eval_schedule_objects(self):
        """
        Computes and returns the number of malus points based on the 
        whole schedule (assigns malus points to individual lessons and students).
        """

        # reset malus points of lessons and courses
        for lesson in self._lessons:
            lesson._malus_points_dict = {"conflicts": 0, "gaps": 0, "capacity": 0, "evening": 0}

        for course in self._courses.values():
            course._malus_points_dict = {"conflicts": 0, "gaps": 0, "capacity": 0, "evening": 0}

        # calculate malus points for each student's individual schedule
        for student in self._students.values():
            
            # reset the malus points to zero
            student._malus_points_dict = {"conflicts": 0, "gaps": 0}

            # create an empty dictionary of timeslots per day
            slots_per_day = {0:[],1:[],2:[],3:[],4:[]}
            
            # loop over all the lessons per student
            for lesson in student.get_lessons():

                # check day and time of lesson and add the timeslot to the correct day
                day = lesson.get_day()
                time = lesson.get_time()
                slots_per_day[day].append(time) 
                        
            # count the malus points for lessons on the same day
            for timeslots in slots_per_day.values():
                if len(timeslots) > 0:

                    # sort the timeslots
                    timeslots.sort()
                                       
                    # calculate the gaps in the timeslots
                    # https://stackoverflow.com/questions/16974047/efficient-way-to-find-missing-elements-in-an-integer-sequence
                    start, end = timeslots[0], timeslots[-1]
                    gaps = sorted(set(range(start, end + 1)).difference(timeslots))  
                    number_of_gaps = len(gaps)

                    # assign 100 malus point for 3 gaps to the student and lesson
                    if number_of_gaps == 3:
                        number_of_gaps = 100 

                    # assign 3 malus points for 2 adjacent gaps
                    if number_of_gaps == 2 and gaps !=  [0, 2, 4]:
                        number_of_gaps = 3

                    # otherwise, assign malus point per gap                        
                    lesson.add_malus_points(number_of_gaps, "gaps")
                    student.add_malus_points(number_of_gaps, "gaps")

                # if timeslots exist multiple times, assign malus points for conflicts   
                if len(timeslots) > len(set(timeslots)):
                    conflicts = len(timeslots) - len(set(timeslots))
                    lesson.add_malus_points(conflicts, "conflicts")
                    student.add_malus_points(conflicts, "conflicts")

        # calculate malus points for each lesson
        for lesson in self._lessons:
            room = lesson.get_room()

            # add malus points for students in lesson exceeding room capacity
            if len(lesson.get_students()) > room.get_capacity():
                excess = len(lesson.get_students()) - room.get_capacity()
                lesson.add_malus_points(excess, "capacity")
            
            # add malus points if evening slot is used
            if room.get_id() == "C0.110":
                time = lesson.get_time()
                if time == 4:
                    lesson.add_malus_points(5, "evening")

            course = lesson.get_course()
            course.add_malus_points(lesson.get_malus_points_dict())

    def get_cell_content(self, loc):
        """
        Returns the contents of a position in the schedule.
        pos = (y, x)
        """

        return self._dataframe.iloc[loc]

    def get_empty_slots(self):
        """
        Return coordinates of empty slots in schedule.
        """

        return [(x, y) for x, y in zip(*np.where(self._dataframe.values == 0))]

    def get_random_loc(self):
        """
        Returns a random location in the schedule.
        """

        index = random.randint(1,145)
        return self._timeslots[index]
        
    def get_courses(self):
        """
        Returns a dictionary of all course objects.
        """
        
        return self._courses

    def get_rooms(self):
        """
        Returns a list of all room objects.
        """

        return self._rooms

    def get_lessons(self):
        """
        Returns a dictionary of all lesson objects.
        """

        return self._lessons

    def get_timeslots(self):
        """
        Returns a dictionary of all timeslots.
        """

        return self._timeslots

    def get_dataframe(self):
        """
        Returns the schedule.
        """

        return self._dataframe

    def is_valid(self):
        """
        Returns whether schedule is valid or not.
        """

        return self._is_valid

    def get_students(self):
        """
        """

        return self._students.values()
