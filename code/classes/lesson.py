class Lesson:

    def __init__(self, name, type, group_number, nr_students):

        # name, type, max students, and students of the lesson
        self._name = name
        self._type = type
        self._group_number = group_number
        self._nr_students = nr_students
        self._students = {}

        # initialize the room and slot
        self._room = None
        self._slot = None

        # number of malus points of lesson
        self._malus_points = {"conflicts": 0, "gaps": 0, "capacity": 0, "evening": 0}

    def has_name(self):
        """
        Returns name of the lesson.
        """

        return self._name

    def has_students(self):
        """
        Returns a dictionary of all students in the lesson.
        """

        return self._students

    def has_nr_students(self):
        """
        Returns the number of students of the lesson.
        """

        return self._nr_students

    def has_room(self):
        """
        Returns the room object the lesson is given in.
        """

        return self._room
    
    def is_type(self):
        """
        Returns the lesson type.
        """

        return self._type

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

    

    def add_student(self, student):
        """
        Adds student to lesson.
        """

        self._students[student.has_number()] = student

    def add_room(self, room):
        """
        Adds room to the lesson.
        """

        self._room = room

    def add_slot(self, slot):
        """
        Adds timeslot to lesson.
        """

        self._slot = slot

    def add_malus_points(self, points, type):
        """
        Adds malus points of given type to the lesson.
        """

        self._malus_points[type] += points
    
    def total_malus_points(self):
        """
        Return the total number of malus points of a lesson.
        """

        return sum(self._malus_points.values())
        
    def __str__(self):
        return f"{self._name} | {self._type} | {self._nr_students} | {len(self._students)} | {self._slot} | {self._room}"

    def __repr__(self):
        return f"{self._name} | {self.total_malus_points()}"