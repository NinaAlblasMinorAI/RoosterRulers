"""
- Programmeertheorie
- RoosterRulers - Lectures & Lesroosters

Student class for all student objects that are
associated with courses and lessons in the schedule.
"""


class Student:

    def __init__(self, name, courses):

        # student name and the names of their registered courses
        self._name = name
        self._courses = courses

        # initial list of associated lessons
        self._lessons = []

        # malus points for the student's individual schedule
        self._malus_points_dict = {"conflicts": 0, "gaps": 0}

    def add_lesson(self, lesson):
        """
        Add lesson to student.
        """

        self._lessons.append(lesson)

    def add_malus_points(self, points, point_type):
        """
        Adds malus points of given type to the student.
        """

        self._malus_points_dict[point_type] += points

    def remove_lesson(self, lesson):
        """
        Removes lesson of student
        """

        self._lessons.remove(lesson)

    def get_courses(self):
        """
        Returns a list of registered courses.
        """

        return self._courses

    def get_name(self):
        """
        Returns the student's name.
        """

        return self._name

    def get_lessons(self):
        """
        Returns a list of student's lessons.
        """

        return self._lessons
