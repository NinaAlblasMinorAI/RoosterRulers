class Lesson:

    def __init__(self, name, nr_students, type):

        # name of the lesson
        self._name = name
        
        # type of the lesson
        self._type = type

        # the max number of students in the lesson
        self._nr_students = nr_students

        # a list of students in the lesson
        self._students = []

        self._slot = 50
        

    def __str__(self):
        return f"{self._name} | {self._type} | {self._nr_students} | {len(self._students)} | {self._slot}"

    def add_student(self, student):
        """Adds student to course."""
        self._students.append(student)
    
    
        

    