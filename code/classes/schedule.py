import csv
import numpy as np
import pandas as pd
# from sklearn.cluster import DBSCAN
from code.algorithms.create_lessons import create_lessons

from code.classes.room import Room
from code.classes.student import Student
from code.classes.course import Course


class Schedule:

    def __init__(self, room_file, student_file, course_file):
        """
        Schedule object that can be visualized.
        """

        # load in all room, student, and course objects
        self._rooms = self.load_rooms(room_file)
        self._students = self.load_students(student_file)
        self._courses = self.load_courses(course_file)

        # add students to each course
        self.add_students_to_courses()

        # initialize empty schedule
        self._dataframe = self.build_empty_schedule()

        self._is_valid = True

        self._lessons = []

    def add_lessons(self, lessons):
        """
        Add the lessons to the schedule
        """
        self._lessons = lessons        

    def load_rooms(self, source_file):
        """
        Loads in all rooms of the schedule.
        """

        rooms = []
        with open(source_file, "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                room = Room(row['\ufeffZaalnummber'], int(row['Max. capaciteit']))
                rooms.append(room)
        
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

        # sort rooms based on capacity
        self._rooms.sort(key=lambda x: x._capacity)

        # build list of all possible time slots (excluding evening slots)
        timeslots = ["Monday 09:00-11:00", "11:00-13:00", "13:00-15:00", "15:00-17:00",
                    "Tuesday 09:00-11:00", "11:00-13:00", "13:00-15:00", "15:00-17:00", 
                    "Wednesday 09:00-11:00", "11:00-13:00", "13:00-15:00", "15:00-17:00", 
                    "Thurday 09:00-11:00", "11:00-13:00", "13:00-15:00", "15:00-17:00", 
                    "Friday 09:00-11:00", "11:00-13:00", "13:00-15:00", "15:00-17:00", ]

        # build schedule without evening slots
        schedule = pd.DataFrame(index=timeslots, columns=self._rooms, data=0)
        
        # add the evening slots (indicated with 1 instead of 0)
        schedule = schedule.reset_index()

        for index in np.arange(3.5, 20.0, 4.0):
            schedule.loc[index] = ["17:00-19:00", "-", "-", "-", "-", "-", "-", 1]

        schedule = schedule.sort_index().reset_index(drop=True)
        schedule.set_index("index", inplace=True)
        schedule.index.names = ["Time"]

        # save schedule
        schedule.to_csv("output_data/empty_schedule.csv")

        return schedule

    def place_lesson(self, lesson, loc):
        """
        Place lesson in specified "zaalslot".
        """

        self._dataframe.iloc[loc]= lesson

    def eval_schedule(self):
        """
        Computes and returns the number of malus points based on the 
        individual schedules of the students and overall schedule.
        """

        malus_points = 0

        # calculate malus points for each student's individual schedule
        for student in self._students.values():

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
                            return None

        

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
            
        self._is_valid = True
        return malus_points

    # def cluster_students(self):
    #     """
    #     Clusters student based on similarity of registered courses.
    #     """

    #     # restructure data to a list of all course lists of students
    #     data = [student.has_courses() for student in self._students]

    #     def lev_metric(x, y):
    #         """Parses the right data to the lev_dist() function."""

    #         i, j = int(x[0]), int(y[0])   
    #         return self.lev_dist(data[i], data[j])

    #     # reshape data and perform clustering based on Levenshein method
    #     X = np.arange(len(data)).reshape(-1, 1)
    #     clustering = DBSCAN(eps=0.5, min_samples=7, metric=lev_metric).fit(X)

    #     core_samples_mask = np.zeros_like(clustering.labels_, dtype=bool)
    #     core_samples_mask[clustering.core_sample_indices_] = True
    #     labels = clustering.labels_
    #     # print(labels)

    #     # Number of clusters in labels, ignoring noise if present.
    #     # n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    #     # n_noise_ = list(labels).count(-1)

    #     # print("Estimated number of clusters: %d" % n_clusters_)
    #     # print("Estimated number of noise points: %d" % n_noise_)


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

    def get_courses(self):
        """
        Returns a dictionary of all course objects.
        """
        
        return self._courses

    def get_rooms(self):
        """
        Returns a dictionary of all room objects.
        """

        return self._rooms

    def get_dataframe(self):
        """
        Returns the schedule.
        """

        return self._dataframe
