"""
- Programmeertheorie
- RoosterRulers - Lectures & Lesroosters

Class for the redistribution of lesson objects in the schedule.
Shuffles lessons randomly.
"""


import random


class RedistributeLessons:

    def __init__(self, algorithm, schedule, nr_repeats, temperature, verbose):

        # set arguments as attributes
        self.algorithm = algorithm
        self.schedule = schedule
        self.repeats = nr_repeats
        self.verbose = verbose

        # keep track of the number of mutations and the scores
        self.counter = 0
        self.best_score = self.schedule.eval_schedule()
        self.new_score = 0

        # initialize list that contains the malus points after each mutation
        self.points_list = [self.best_score]

        # set temperature for the simmulated annealing
        self.start_temperature = temperature
        self.temperature = self.start_temperature

        # execute specified algorithm, raise ValueError if it does not exist
        if self.algorithm == "hillclimber":
            self.hillclimber()
        elif self.algorithm == "simulated_annealing":
            self.simulated_annealing()
        else:
            raise ValueError("Specified algorithm does not exist for requested mutation")

    def hillclimber(self):
        """
        Mutates the schedule until objective value does not improve <nr_repeats> times.
        """

        while self.counter < self.repeats:

            # swap random lessons and evaluate
            locations = self.swap_random_lessons()

            # print result if verbose
            if self.verbose:
                self.print_result("Lesson")

            # valuate change in schedule and act accordingly.
            self.evaluate(locations)

            # add current best score to list
            self.points_list.append(self.best_score)

    def simulated_annealing(self):
        """
        Mutates the schedule and accepts changes according to chance function.
        """

        # run as long as the repeats are not reached, and the temperature is above 0.01 (to avoid dumps)
        while self.counter < self.repeats and self.temperature > 0.01:

            # swap lesson and print results
            locations = self.swap_random_lessons()

            # print result if verbose
            if self.verbose:
                self.print_result("Lesson")

            # use try-except, because there is an overflow if the difference between old and new points is too large
            try:
                # if the random number is higher than the chance, reverse the swap
                chance = self.calc_chances()
                if random.random() > chance:
                    self.revert_change(locations)
                else:
                    self.best_score = self.new_score
            except OverflowError as e:
                if self.verbose:
                    print("OverFlowError: ", e)

                # set best score to the points of the new schedule (error occured because of a large difference)
                self.best_score = self.schedule.eval_schedule()

            # add current best score to list
            self.points_list.append(self.best_score)

            # increase the counter
            self.counter += 1

            # adjust the temperature
            self.adjust_temperature()

    def swap_random_lessons(self):
        """
        Takes two random lessons and swaps their positions.
        Evaluates the updated schedule and returns its points.
        """

        # get two random locations in the schedule
        loc1 = self.schedule.get_random_loc()
        loc2 = self.schedule.get_random_loc()

        # swap the contents of the random locations and evaluate
        self.schedule.swap_contents(loc1, loc2)
        self.new_score = self.schedule.eval_schedule()

        # return the locations
        return (loc1, loc2)

    def evaluate(self, args):
        """
        Evaluate change in schedule and act accordingly.
        """

        if self.new_score > self.best_score:
            self.revert_change(args)
            self.counter += 1
        elif self.new_score == self.best_score:
            self.counter += 1
        else:
            self.best_score = self.new_score
            self.counter = 0

    def revert_change(self, locations):
        """
        Reverts the change after not obtaining a better score.
        """

        self.schedule.swap_contents(locations[0], locations[1])

    def calc_chances(self):
        """
        Calculates the chances of a change being accepted in simulated annealing.
        """

        chance = 2 ** ((self.best_score - self.new_score) / self.temperature)
        return chance

    def adjust_temperature(self):
        """
        Adjusts the temperature of the simmulated annealing after an iteration.
        """

        self.temperature = self.start_temperature - ((self.start_temperature / self.repeats) * self.counter)

    def print_result(self, mutation):
        """
        Prints the result after a mutation.
        """

        print(f"{mutation} redistribution, {self.algorithm}: New points: {self.new_score}  |  Lowest points: {self.best_score}")
        if self.algorithm == "simulated_annealing":
            print(f"{mutation} redistribution, {self.algorithm}: Run: {self.counter}  |   Temperature: {self.temperature}")

    def get_schedule(self):
        return self.schedule

    def get_points(self):
        return self.points_list
