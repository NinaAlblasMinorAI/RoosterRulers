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
        Schedule object that can be visualized.
        """

        # load in all room, student, and course objects
        self._rooms = self.load_rooms("input_data/rooms.csv")
        self._students = self.load_students("input_data/students.csv")
        self._courses = self.load_courses("input_data/courses.csv")

        # add students to each course
        self.add_students_to_courses()

        # initialize empty schedule
        self._dataframe = None
        self._timeslots = {}
        self.build_empty_schedule()

        # create and place lessons
        self._lessons = self.create_lessons()
        self.place_lessons_randomly()

        # boolean to check if a schedule is valid
        self._is_valid = True  

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

        # FYI: sorting the rooms has been moved to load_rooms()

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

        # save schedule
        schedule.to_csv("output_data/empty_schedule.csv")

        self._dataframe = schedule

        # create time slots
        counter = 1
        for x in range(7):
            if x == 6:
                for y in range(25):
                    self._timeslots[counter] = (y, x)
                    counter += 1
            else:
                for y in range(25):
                    if (y + 1) % 5 == 0:
                        continue
                    self._timeslots[counter] = (y, x)
                    counter += 1

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
            lesson_name = f"{course.get_name()}"
            lesson_type = "lecture"
            lesson_group_nr = i + 1
            max_nr_students = None
            
            # create the lesson
            lesson = Lesson(lesson_name, lesson_type, lesson_group_nr, max_nr_students)
            lectures.append(lesson)

            # associate the lesson with students
            students = course.get_students()
            for student in students:
                lesson.add_student(student)
        
        return lectures

    def create_tutos_and_labs(self, course, type):
        """
        Creates the tutorial or lab lessons for a course.
        """

        # copy the students from the course, so that they can be devided
        students = list(course.get_students()).copy()

        # calculate the number of lessons and students per lesson
        max_students = course.get_max_students(type)
        number_of_lessons = math.ceil(len(students) / max_students)
        students_per_lesson = math.ceil(len(students) / number_of_lessons) 

        # create the lessons
        lessons = []
        for i in range(number_of_lessons):
            
            # create lesson attributes
            lesson_name = f"{course.get_name()}"
            lesson_type = type
            lesson_group_nr = i + 1
            
            # create the lesson
            lesson = Lesson(lesson_name, lesson_type, lesson_group_nr, max_students)
            lessons.append(lesson)
            
            for j in range(students_per_lesson):
                if len(students) > 0:

                    # add lesson to student and student to lesson
                    student = students.pop()
                    student.add_lesson(lesson)
                    lesson.add_student(student)

        return lessons

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

    def place_content(self, lesson, loc):
        """
        Place lesson in specified "zaalslot".
        loc = (y, x)
        """

        # set time slot and add room to lesson if present
        if isinstance(lesson, Lesson):
            slot = loc[0] + 1
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
            
            # remove students from both lessons
            lesson1.remove_student(student1)
            lesson2.remove_student(student2)

            # remove lessons from both students
            student1.remove_lesson(lesson1)
            student2.remove_lesson(lesson2)

            # add students to lessons the other way
            lesson1.add_student(student2)
            lesson2.add_student(student1)

            # add lessons to students
            student1.add_lesson(lesson2)
            student2.add_lesson(lesson1)
        elif student1 is not None and student2 is None:
            lesson1.remove_student(student1)
            student1.remove_lesson(lesson1)
            lesson2.add_student(student1)
            student1.add_lesson(lesson2)
        elif student2 is not None and student1 is None:
            lesson2.remove_student(student2)
            student2.remove_lesson(lesson2)
            lesson1.add_student(student2)
            student2.add_lesson(lesson1)
        else:
            pass

    def eval_schedule(self):
        """
        Computes and returns the number of malus points based on the 
        individual schedules of the students and overall schedule.
        """

        malus_points = 0

        # calculate malus points for each student's individual schedule
        for student in self._students.values():

            # reset malus points of student
            student._malus_points_dict = {"conflicts": 0, "gaps": 0}

            # build personal schedule
            schedule = []

            # go over each registered lesson
            for lesson in student.get_lessons():

                # check day and time of lesson and add to slot
                slot = {}
                slot["day"] = lesson.get_day()
                slot["time"] = lesson.get_time()
                schedule.append(slot)
            
            # check the time between every combination of lessons
            for i in range(len(schedule)):
                anker_day = schedule[i]["day"] 
                anker_time = schedule[i]["time"]

                for j in range(i+1, len(schedule)):
                    comp_day = schedule[j]["day"]
                    comp_time = schedule[j]["time"]

                    # only count malus points if lessons are given on the same day
                    if anker_day == comp_day:
                        lesson = student.get_lessons()[i]
                        if anker_time == comp_time:             # if course conflict, 1 malus point
                            lesson.add_malus_points(1, "conflicts")
                            student.add_malus_points(1, "conflicts")
                        elif abs(anker_time - comp_time) == 2:  # if 1 time slot in between, 1 malus point
                            lesson.add_malus_points(1, "gaps")
                            student.add_malus_points(1, "gaps")
                        elif abs(anker_time - comp_time) == 3:  # if 2 time slots in between, 3 malus points
                            lesson.add_malus_points(3, "gaps")
                            student.add_malus_points(3, "gaps")
                        elif abs(anker_time - comp_time) > 3:   # schedules with 3 time slots in between are not valid
                            self._is_valid = False
                            lesson.add_malus_points(100, "gaps")
                            student.add_malus_points(100, "gaps")

        # calculate malus points for each lesson
        for lesson in self._lessons:

            # obtain room of lesson
            room = lesson.get_room()

            # add malus points for students in lesson exceeding room capacity
            if len(lesson.get_students()) > room.get_capacity():
                excess = len(lesson.get_students()) - room.get_capacity()
                lesson.add_malus_points(excess, "capacity")
            
            # add malus points if evening slot is used
            if room.get_id() == "C0.110":
                time = lesson.get_time()
                if time == 0:
                    lesson.add_malus_points(5, "evening")

            malus_points += lesson.get_malus_points()
            
            # reset malus points of each lesson
            lesson._malus_points_dict = {"conflicts": 0, "gaps": 0, "capacity": 0, "evening": 0}
            
        self._is_valid = True
        return malus_points

    def cluster_students(self):
        """
        Clusters student based on similarity of registered courses.
        """

        # restructure data to a list of all course lists of students
        data = [student.has_courses() for student in self._students]

        def lev_metric(x, y):
            """Parses the right data to the lev_dist() function."""

            i, j = int(x[0]), int(y[0])   
            return self.lev_dist(data[i], data[j])

        # reshape data and perform clustering based on Levenshein method
        X = np.arange(len(data)).reshape(-1, 1)
        clustering = DBSCAN(eps=0.5, min_samples=7, metric=lev_metric).fit(X)

        core_samples_mask = np.zeros_like(clustering.labels_, dtype=bool)
        core_samples_mask[clustering.core_sample_indices_] = True
        labels = clustering.labels_

        # Number of clusters in labels, ignoring noise if present.
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise_ = list(labels).count(-1)

        print("Estimated number of clusters: %d" % n_clusters_)
        print("Estimated number of noise points: %d" % n_noise_)

    def lev_dist(self, source, target):
        """Computes the Levenshein distance between two lists of strings"""

        if source == target:
            return 0

        # Prepare matrix
        slen, tlen = len(source), len(target)
        dist = [[0 for i in range(tlen+1)] for x in range(slen+1)]
        for i in range(slen+1):
            dist[i][0] = i
        for j in range(tlen+1):
            dist[0][j] = j

        # Counting distance
        for i in range(slen):
            for j in range(tlen):
                cost = 0 if source[i] == target[j] else 1
                dist[i+1][j+1] = min(
                                dist[i][j+1] + 1,   # deletion
                                dist[i+1][j] + 1,   # insertion
                                dist[i][j] + cost   # substitution
                            )
        return dist[-1][-1]

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