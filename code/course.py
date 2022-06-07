class Course:

    def __init__(self, name, E_students, nr_lect, nr_tuto, max_students_tuto, nr_lab, max_students_lab):

        # name, number of students and student objects of the course
        self._name = name
        self._E_students = E_students
        self._students = []

        # number of course activities to be divided
        self._nr_lect = nr_lect
        self._nr_tuto = nr_tuto
        self._nr_lab = nr_lab

        # maximum group size for tutorials and labs
        self._max_students_tuto = max_students_tuto
        self._max_students_lab = max_students_lab

        # optional lab and tutorial groups
        if self._nr_tuto > 0:
            self._tuto_groups = []
        if self._nr_lab > 0:
            self._lab_groups = []

    def add_student(self, student):
        """Adds student to course."""

        self._students.append(student)
    
    # Return course expect number of students id
    def get_expected_students(self):
        return self._E_students

    