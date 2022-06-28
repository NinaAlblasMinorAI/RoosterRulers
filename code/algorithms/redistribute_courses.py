"""
- Programmeertheorie
- RoosterRulers - Lectures & Lesroosters

Class for creating additional lesson objects of courses in the schedule.
"""


import random

from code.algorithms.redistribute_lessons import RedistributeLessons
from code.classes.lesson import Lesson


class RedistributeCourses(RedistributeLessons):

    def __init__(self, algorithm, schedule, nr_courses, verbose):

        # set arguments as attributes
        self.algorithm = algorithm
        self.schedule = schedule
        self.nr_courses = nr_courses
        self.verbose = verbose

        # initialize list that contains the malus points after each mutation
        self.points_list = [self.schedule.eval_schedule(False)]

        # execute specified algorithm, raise ValueError if it does not exist
        if self.algorithm == "greedy":
            self.greedy()
        else:
            raise ValueError

    def greedy(self):
        """
        Takes the courses with the most malus points
        and divides its lesson with the most malus points into two.
        """

        # get the x courses with the most malus points
        worst_courses = self.get_worst_courses()

        # obtain empty slots in schedule and shuffle
        empty_slots = self.schedule.get_empty_slots()
        random.shuffle(empty_slots)

        # split of an extra lesson for each course
        for course in worst_courses:

            # get worst lesson of course
            worst_lesson = self.get_worst_lesson(course)

            # create new lesson object
            new_lesson = self.create_new_lesson(course, worst_lesson)

            # transfer half of students to new lesson
            self.transfer_students(worst_lesson, new_lesson)

            # place new lesson in a random empty slot in schedule
            random_loc = empty_slots.pop()
            self.schedule.place_content(new_lesson, random_loc)

            # print result if verbose
            if self.verbose:
                self.print_result("Course")

            # add schedule score to list
            malus_points = self.schedule.eval_schedule(False)
            self.points_list.append(malus_points)

    def get_worst_courses(self):
        """
        Get list of courses with the most malus points
        that have tutorials or labs.
        """

        # evaluate course objects in schedule
        self.schedule.eval_schedule(True)

        # obtain list of all courses
        courses = [course for course in self.schedule.get_courses().values()
                   if course.get_nr_lessons("tutorial") > 0
                   or course.get_nr_lessons("lab") > 0]

        # sort courses based on malus points and return the x worst courses
        courses.sort(key=lambda x: x.get_malus_points(), reverse=True)
        return courses[:self.nr_courses]

    def get_worst_lesson(self, course):
        """
        Get the worst lesson of a course.
        """

        # obtain all tutorials and labs of the course
        lessons = [lesson for lesson in self.schedule.get_lessons()
                   if lesson.get_course() == course
                   and lesson.get_type() != "lecture"]

        # sort lessons based on malus points and return worst lesson
        lessons.sort(key=lambda x: x.get_malus_points(), reverse=True)
        return lessons[0]

    def create_new_lesson(self, course, lesson):
        """
        Creates new lesson object split off from existing lesson.
        """

        # create lesson attributes
        lesson_name = lesson.get_name()
        lesson_type = lesson.get_type()
        lesson_group_nr = course.get_nr_groups(lesson_type) + 1
        max_nr_students = lesson.get_max_students()

        # create the lesson
        new_lesson = Lesson(lesson_name, lesson_type, lesson_group_nr, max_nr_students, course)

        # add lesson to schedule and group nr to course
        self.schedule.add_extra_lesson(new_lesson)
        course.add_group(lesson_type)

        # return lesson
        return new_lesson

    def transfer_students(self, worst_lesson, new_lesson):
        """
        Transfer half of the students from worst lesson to new lesson.
        """

        # get half of the students from old lesson
        all_students = worst_lesson.get_students()
        nr_students = int(len(all_students)/2)
        half_students = all_students[:nr_students]

        # transfer the students to new lesson
        for student in half_students:

            # remove student from old lesson and old lesson from student
            worst_lesson.remove_student(student)
            student.remove_lesson(worst_lesson)

            # add student to new lesson and new lesson to student
            new_lesson.add_student(student)
            student.add_lesson(new_lesson)
