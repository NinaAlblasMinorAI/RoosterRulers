class Student:

    def __init__(self, name, number, courses):
        """
        Student object that is associated with courses and lessons in the schedule.
        """

        # student name, number and the names of their registered courses
        self._name = name
        self._number = number
        self._courses = courses
        self._lessons = []

        # malus points for the student's individual schedule
        self._malus_points_dict = {"conflicts": 0, "gaps": 0}

    def get_courses(self):
        """
        Returns a list of registered courses.
        """

        return self._courses

    def get_lessons(self):
        """
        Returns a list of student's lessons.
        """

        return self._lessons

    def get_number(self):
        """
        Returns the student number.
        """

        return self._number

    def add_lesson(self, lesson):
        """
        Add lesson to student.
        """

        self._lessons.append(lesson)

    def add_malus_points(self, points, type):
        """
        Adds malus points of given type to the student.
        """

        self._malus_points_dict[type] += points

    def get_malus_points(self):
        """
        Return the total number of malus points of a student.
        """

        return sum(self._malus_points_dict.values())