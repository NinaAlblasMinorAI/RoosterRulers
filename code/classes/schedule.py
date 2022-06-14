import csv
import math
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN

from code.classes.room import Room
from code.classes.student import Student
from code.classes.course import Course
from code.classes.lesson import Lesson


class Schedule:

    def __init__(self, room_file, student_file, course_file):
        """
        Schedule object that can be visualized.
        """

        # load in all room, student, and course objects and initialize dict for lessons
        self._rooms = self.load_rooms(room_file)
        self._students = self.load_students(student_file)
        self._courses = self.load_courses(course_file)
        self._lessons = {}

        # add students to each course
        self.add_students_to_courses()

        # initialize empty schedule
        self._schedule = self.build_empty_schedule()


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
            for course_name in student.has_courses():
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

    def fill_schedule(self):
        """
        Fills schedule with lessons.
        """

        # # sort courses based on number of students
        # self._courses.sort(key=lambda x: x._E_students, reverse=True)

        # # start with the lesson with the largest number of students
        # lessons.sort(key=lambda x: x._nr_students, reverse=True)

        # create lesssons and place in schedule
        for course in self._courses.values():
            course_lessons = self.create_lessons(course)
            self.place_lessons(course_lessons)

    def place_lessons(self, lessons):
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
            while number_of_students > self._rooms[x].has_capacity() or self._schedule.iloc[y,x] != 0 or y in forbidden_y_lectures:
            # while number_of_students > rooms[x].get_capacity() or schedule.iloc[y,x] != 0:
                x += 1
        
                # after the last room, go to the next time slot
                if x == 7:
                    y += 1
                    x = 0
                
                if lesson.is_type() == "lab":
                    while y in forbidden_y_tutorials:
                        y += 1
            
            # add the room to the lesson
            lesson.add_room(self._rooms[x])
            if lesson.is_type() == "lecture":
                forbidden_y_lectures.append(y)
            if lesson.is_type() == "tutorial":
                forbidden_y_tutorials.append(y)
            
            # add the course to the schedule
            self._schedule.iloc[y,x]= lesson
            lesson.add_slot(y + 1)

    def create_lessons(self, course):
        """
        Create lesson objects of course.
        """

        course_lessons = []

        # create the lectures
        lectures = self.create_lectures(course)
        course_lessons.extend(lectures)

        # create the tutorials
        if course.has_nr_lessons("tutorial") == 1:
            tutorials = self.create_tutos_and_labs(course, "tutorial")
            course_lessons.extend(tutorials)

        # create the labs
        if course.has_nr_lessons("lab") == 1:
            labs = self.create_tutos_and_labs(course, "lab")
            course_lessons.extend(labs)
        
        return course_lessons

    def create_lectures(self, course):
        """
        Creates the lecture lessons for a course.
        """

        lessons = []
        for i in range(course.has_nr_lessons("lecture")):

            # create name of lesson and set nr students equal to students in course
            lesson_name = f"{course.has_name()}({i + 1})"
            lesson_nr_students = len(course.has_students())
            lesson_type = "lecture"

            # create the lesson
            lesson = Lesson(lesson_name, lesson_nr_students, lesson_type)

            # associate the lesson with students
            students = course.has_students()
            for student in students:
                lesson.add_student(student)

            # append the lesson to the dictionary of lessons
            self._lessons[lesson_name] = lesson
            lessons.append(lesson)
        
        return lessons

    def create_tutos_and_labs(self, course, type):
        """
        Creates the tutorial and lab lessons for a course.
        """

        # copy the students from the course, so that they can be devided
        students = list(course.has_students()).copy()

        # calculate the number of lessons and students per lesson
        number_of_lessons = math.ceil(len(students) / course.has_max_students(type))
        students_per_lesson = math.ceil(len(students) / number_of_lessons) 

        # create the lessons
        lessons = []
        for i in range(number_of_lessons):

            lesson_name = f"{course.has_name()}({i + 1})"
            lesson_nr_students = students_per_lesson
            lesson_type = type

            # create the lesson
            lesson = Lesson(lesson_name, lesson_nr_students, lesson_type)
            for j in range(lesson_nr_students):
                if len(students) > 0:

                    # add lesson to student and student to lesson
                    student = students.pop()
                    student.add_lesson(lesson)
                    lesson.add_student(student)
            
            # add the lesson to the dictionary of lessons 
            self._lessons[lesson_name] = lesson
            lessons.append(lesson)

        return lessons

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
            for lesson in student.has_lessons():

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
                        lesson = student.has_lessons()[i]
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
                            raise ValueError('There are three in-between time slots for the student (invalid schedule)')

        # calculate malus points for each lesson
        for lesson in self._lessons.values():

            # obtain room of lesson
            room = lesson.has_room()

            # add malus points for students in lesson exceeding room capacity
            if len(lesson.has_students()) > room.has_capacity():
                excess = len(lesson.has_students()) - room.has_capacity()
                lesson.add_malus_points(excess, "capacity")
            
            # add malus points if evening slot is used
            if room.has_id() == "C0.110":
                time = lesson.get_time()
                if time == 0:
                    lesson.add_malus_points(5, "evening")

            malus_points += lesson.total_malus_points()

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
        # print(labels)

        # Number of clusters in labels, ignoring noise if present.
        # n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        # n_noise_ = list(labels).count(-1)

        # print("Estimated number of clusters: %d" % n_clusters_)
        # print("Estimated number of noise points: %d" % n_noise_)


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

    def has_rooms(self):
        """
        Returns a dictionary of all room objects.
        """

        return self._rooms

    def has_courses(self):
        """
        Returns a dictionary of all course objects.
        """
        
        return self._courses

    def has_students(self):
        """
        Returns a dictionary of all student objects.
        """

        return self._students

    def has_lessons(self):
        """
        Returns a dictionary of all lesson objects.
        """

        return self._lessons