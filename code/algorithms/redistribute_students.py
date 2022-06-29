"""
- Programmeertheorie
- RoosterRulers - Lectures & Lesroosters

Class for the redistribution of student objects in the schedule.
Shuffles students between lessons of the same course and lesson type.
"""


import random
from code.algorithms.redistribute_lessons import RedistributeLessons


class RedistributeStudents(RedistributeLessons):

    def __init__(self, algorithm, schedule, nr_outer_repeats, nr_inner_repeats, verbose):

        # set arguments as attributes
        self.algorithm = algorithm
        self.schedule = schedule
        self.outer_repeats = nr_outer_repeats
        self.inner_repeats = nr_inner_repeats
        self.verbose = verbose

        # keep track of the number of mutations and the scores
        self.outer_counter = 0
        self.counter = 0
        self.outer_best_score = self.schedule.eval_schedule()
        self.best_score = self.outer_best_score
        self.outer_new_score = 0
        self.new_score = 0

        # initialize list that contains the malus points after each mutation
        self.points_list = [self.outer_best_score]

        # initialize list of lessons of the same course and type
        self.lessons = []

        # execute specified algorithm, raise ValueError if it does not exist
        if self.algorithm == "hillclimber":
            self.hillclimber()
        else:
            raise ValueError("Specified algorithm does not exist for requested mutation")

    def hillclimber(self):
        """
        Mutates the schedule until objective value does not improve <nr_outer_repeats> times.
        """

        while self.outer_counter < self.outer_repeats:

            # reset inner counter and best score
            self.counter = 0
            self.best_score = self.outer_best_score

            # get all tutorials or labs of a random course
            self.get_course_lessons()

            # randomly swap students between lessons based on hillclimber
            while self.counter < self.inner_repeats:

                if len(self.lessons) > 1:

                    # swap two random students (or spots) of lessons
                    students_lessons = self.swap_students()

                    # print result if verbose
                    if self.verbose:
                        self.print_result("Student")

                    # evaluate change in schedule and act accordingly.
                    self.evaluate(students_lessons)

                    # add current best score to list
                    self.points_list.append(self.best_score)

            # check if changes to the lessons of one course had effect
            self.outer_new_score = self.best_score
            if self.outer_new_score >= self.outer_best_score:
                self.outer_counter += 1
            else:
                self.outer_best_score = self.outer_new_score
                self.outer_counter = 0

    def get_course_lessons(self):
        """
        Returns all lessons of the same type of a random course.
        """

        # obtain random tutorial or lab
        tutos_and_labs = [lesson for lesson in self.schedule.get_lessons()
                          if lesson.get_type() != "lecture"]
        random.shuffle(tutos_and_labs)
        random_lesson = tutos_and_labs[0]

        # get all other tutorials or labs of that course
        self.lessons = [lesson for lesson in self.schedule.get_lessons()
                        if lesson.get_name() == random_lesson.get_name()
                        and lesson.get_type() == random_lesson.get_type()]

    def swap_students(self):
        """
        Shuffle the students of the lessons and evaluate mutated schedule.
        """

        # randomly pick two different lessons
        lesson1, lesson2 = self.pick_two_lessons()

        # randomly pick two students (or empty spots)
        student1, student2 = self.pick_two_students(lesson1, lesson2)

        # swap students between lessons and evaluate
        self.schedule.swap_students(student1, lesson1, student2, lesson2)
        self.new_score = self.schedule.eval_schedule()

        # return the swapped students and associated lessons
        return (student1, lesson2, student2, lesson1)

    def pick_two_lessons(self):
        """
        Randomly picks two different lessons.
        """

        # return two random lessons
        random_lessons = random.sample(self.lessons, 2)
        return random_lessons[0], random_lessons[1]

    def pick_two_students(self, lesson1, lesson2):
        """
        Radomly picks two students (or not) to be swapped.
        """

        # get random index of list of student slots of lesson
        index_student1 = random.randint(0, lesson1.get_max_students() - 1)
        index_student2 = random.randint(0, lesson2.get_max_students() - 1)

        # check if the slots at those indices contain students, set None if not
        if index_student1 + 1 > lesson1.get_nr_students():
            student1 = None
        else:
            student1 = lesson1.get_students()[index_student1]

        if index_student2 + 1 > lesson2.get_nr_students():
            student2 = None
        else:
            student2 = lesson2.get_students()[index_student2]

        # return the students (or None's)
        return student1, student2

    def revert_change(self, students_lessons):
        """
        Reverts the change after not obtaining a better score.
        """

        self.schedule.swap_students(students_lessons[0], students_lessons[1],
                                    students_lessons[2], students_lessons[3])
