class Lesson:

    def __init__(self, name, type, group_number, max_nr_students, course):

        # name, type, max students, and students of the lesson
        self._name = name
        self._type = type
        self._group_number = group_number
        self._max_nr_students = max_nr_students
        self._course = course
        self._students = []

        # initialize the room and slot
        self._room = None
        self._slot = None

        # number of malus points of lesson
        self._malus_points_dict = {"conflicts": 0, "gaps": 0, "capacity": 0, "evening": 0}

    def get_name(self):
        """
        Returns name of the lesson.
        """

        return self._name

    def get_students(self):
        """
        Returns a list of all students in the lesson.
        """

        return self._students

    def get_max_students(self):
        """
        Returns the maximum number of students in lesson.
        """

        return self._max_nr_students

    def get_nr_students(self):
        """
        Returns the number of students of the lesson.
        """

        return len(self._students)

    def get_room(self):
        """
        Returns the room object the lesson is given in.
        """

        return self._room
    
    def get_type(self):
        """
        Returns the lesson type.
        """

        return self._type

    def get_group_nr(self):
        """
        Returns the lesson group number.
        """

        return self._group_number

    def get_day(self):
        """
        Returns the day the lesson is given.
        """

        return int(self._slot / 5)

    def get_time(self):
        """
        Returns the time the lesson is given.
        """

        return self._slot % 5

    def get_malus_points(self):
        """
        Return the total number of malus points of a lesson.
        """

        return sum(self._malus_points_dict.values())

    def get_malus_points_dict(self):
        """
        Return the dictionary of malus points of a lesson.
        """

        return self._malus_points_dict

    def get_course(self):
        """
        Returns the course object associated with the lesson.
        """

        return self._course

    def add_student(self, student):
        """
        Adds student to lesson.
        """

        self._students.append(student)

    def remove_student(self, student):
        """
        Removes student from lesson.
        """

        self._students.remove(student)

    def set_room(self, room):
        """
        Adds room to the lesson.
        """

        self._room = room

    def set_slot(self, slot):
        """
        Adds timeslot to lesson.
        """

        self._slot = slot

    def add_malus_points(self, points, type):
        """
        Adds malus points of given type to the lesson.
        """

        self._malus_points_dict[type] += points
        
    def __str__(self):
        # return f"{self._name} | {self._type} | {self._group_number} | {len(self._students)} | {self._slot} | {self._room}"
        if self._type == "lecture":
            lesson_type = "h"
        elif self._type == "tutorial":
            lesson_type = "w"
        elif self._type == "lab":
            lesson_type = "p"
        
        if int((self._slot) / 5) == 0:
            day = "ma"
        if int((self._slot) / 5) == 1:
            day = "di"
        if int((self._slot) / 5) == 2:
            day = "wo"
        if int((self._slot) / 5) == 3:
            day = "do"
        if int((self._slot) / 5) == 4:
            day = "vr"
        
        if int((self._slot) % 5) == 0:
            time = 9
        if int((self._slot) % 5) == 1:
            time = 11
        if int((self._slot) % 5) == 2:
            time = 13
        if int((self._slot) % 5) == 3:
            time = 15
        if int((self._slot) % 5) == 4:
            time = 17

        return f"{self._name},{lesson_type}{self._group_number},{self._room},{day},{time}"

    def __repr__(self):
        return f"{self._name} | {self.get_malus_points()}"
