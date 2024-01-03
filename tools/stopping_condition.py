import time


class StoppingCondition:
    def __init__(self):
        self.time_limit = 300  # 5 minutes in seconds
        self.fitness_threshold = 0.12
        self.stop_execution = False

    def check_time_limit(self, start_time):
        return time.time() - start_time > self.time_limit

    def check_fitness_threshold(self, fitness):
        return fitness < self.fitness_threshold

    def should_stop(self, start_time, fitness):
        return self.check_time_limit(start_time) or self.check_fitness_threshold(fitness)