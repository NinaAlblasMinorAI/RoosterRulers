"""
- Programmeertheorie
- RoosterRulers - Lectures & Lesroosters

Course class for all course objects in the schedule that will
be divided into different lessons (lectures, tutorials, and labs).
"""


class Course:

    def __init__(self, name, nr_lect, nr_tuto, max_students_tuto, nr_lab, max_students_lab):

        # name and student objects of the course
        self._name = name
        self._students = []

        # number of course activities to be divided
        self._nr_lect = nr_lect
        self._nr_tuto = nr_tuto
        self._nr_lab = nr_lab

        # maximum group size for tutorials and labs
        self._max_students_tuto = max_students_tuto
        self._max_students_lab = max_students_lab

        # initial number of tutorial and lab groups
        self._tuto_groups = 0
        self._lab_groups = 0

        # number of malus points of course
        self._malus_points_dict = {"conflicts": 0, "gaps": 0, "capacity": 0, "evening": 0}

    def add_student(self, student):
        """
        Adds student to course.
        """

        self._students.append(student)

    def add_group(self, type):
        """
        Adds one to the number of groups attribute.
        """

        if type == "tutorial":
            self._tuto_groups += 1
        else:
            self._lab_groups += 1

    def add_malus_points(self, dict):
        """
        Adds the malus points of a lesson to the course.
        """

        for key in dict:
            self._malus_points_dict[key] += dict[key]

    def get_nr_lessons(self, lesson_type):
        """
        Returns the number of lessons for the specified lesson type.
        """

        if lesson_type == "lecture":
            return self._nr_lect
        elif lesson_type == "tutorial":
            return self._nr_tuto
        else:
            return self._nr_lab

    def get_max_students(self, lesson_type):
        """
        Returns the max number of students for specified lesson type.
        """

        if lesson_type == "tutorial":
            return self._max_students_tuto
        else:
            return self._max_students_lab

    def get_name(self):
        """
        Returns the name of the course.
        """

        return self._name

    def get_nr_students(self):
        """
        Returns the absolute number of students of the course.
        """

        return len(self.students)

    def get_students(self):
        """
        Returns a list of registered students.
        """

        return self._students

    def get_nr_groups(self, lesson_type):
        """
        Returns the number of groups of specified lesson type.
        """

        if lesson_type == "tutorial":
            return self._tuto_groups
        else:
            return self._lab_groups

    def get_malus_points(self):
        """
        Return the total number of malus points of a lesson.
        """

        return sum(self._malus_points_dict.values())

    def __str__(self):
        return f"{self._name} | {self.get_nr_students()}"
