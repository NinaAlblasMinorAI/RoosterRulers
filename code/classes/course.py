class Course:

    def __init__(self, name, E_students, nr_lect, nr_tuto, max_students_tuto, nr_lab, max_students_lab):
        """
        Course object to be divided into lessons.
        """

        # name, number of students and student objects of the course
        self._name = name
        self._E_students = E_students
        self._students = {}
        
        # number of course activities to be divided
        self._nr_lect = nr_lect
        self._nr_tuto = nr_tuto
        self._nr_lab = nr_lab
        
        # maximum group size for tutorials and labs
        if self._nr_tuto != 0:
            self._max_students_tuto = max_students_tuto
        if self._nr_lab != 0:
            self._max_students_lab = max_students_lab

    def get_E_students(self):
        """
        Returns the expected number of students in the course.
        """

        return self._E_students

    def get_nr_lessons(self, type):
        """
        Returns the number of lessons for specified lesson type.
        """

        if type == "lecture":
            return self._nr_lect
        elif type == "tutorial":
            return self._nr_tuto
        else:
            return self._nr_lab

    def get_max_students(self, type):
        """
        Returns the max number of students for specified lesson type.
        """ 

        if type == "tutorial":
            return self._max_students_tuto
        else:
            return self._max_students_lab       

    def get_name(self):
        """
        Returns the name of the course.
        """

        return self._name

    def get_students(self):
        """
        Returns a list of registered students.
        """

        return self._students.values()

    def add_student(self, student):
        """
        Adds student to course.
        """

        self._students[student.has_number()] = student

    def __str__(self):
        """
        Representation of object as a string.
        """

        return f"{self._name} | {self._E_students} | {len(self._students)} "
    