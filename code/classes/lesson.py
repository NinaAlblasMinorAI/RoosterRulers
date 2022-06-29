"""
- Programmeertheorie
- RoosterRulers - Lectures & Lesroosters

Lesson class for all lesson objects in the schedule made from course objects
that were divided into different lessons (lectures, tutorials, and labs).
"""


class Lesson:

    def __init__(self, name, type, group_number, max_nr_students, course):

        # name, type, group number, and max students of the lesson
        self._name = name
        self._type = type
        self._group_number = group_number
        self._max_nr_students = max_nr_students

        # course associated to the lesson and the lesson's students
        self._course = course
        self._students = []

        # initialize the room and slot
        self._room = None
        self._slot = None   # kan veranderd worden naar de locatie

        # number of malus points of lesson
        self._malus_points_dict = {"conflicts": 0, "gaps": 0, "capacity": 0, "evening": 0}

    def add_student(self, student):
        """
        Adds student to lesson.
        """

        self._students.append(student)

    def add_malus_points(self, points, point_type):
        """
        Adds malus points of given type to the lesson.
        """

        self._malus_points_dict[point_type] += points

    def remove_student(self, student):
        """
        Removes student from lesson.
        """

        self._students.remove(student)

    def set_room(self, room):
        """
        Sets the room of the lesson.
        """

        self._room = room

    def set_slot(self, slot):
        """
        Sets timeslot of lesson.
        """

        self._slot = slot

    def get_name(self):
        """
        Returns name of the lesson.
        """

        return self._name

    def get_nr_students(self):
        """
        Returns the number of students of the lesson.
        """

        return len(self._students)

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
        Returns the relative day the lesson is given as an int (0-4).
        """

        return int(self._slot / 5)

    def get_time(self):
        """
        Returns the relative time the lesson is given as an int (0-4).
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

    def __str__(self):
        return f"{self._name} | {self.get_malus_points()}"

        
    def __repr__(self):
        return f"{self._name} | {self.get_malus_points()}"
