import numpy as np


def generate_valid_population_and_elitism(population_bounds, elitism_bounds):
    while True:
        # Generate random values for population size and elitism size
        new_population_size = np.random.randint(low=population_bounds[0], high=population_bounds[1] + 1)
        new_elitism_size = np.random.randint(low=elitism_bounds[0],
                                             high=min(elitism_bounds[1], new_population_size - 1) + 1)

        # Check if conditions are met
        if new_population_size % 4 == 0 and new_elitism_size % 2 == 0:
            return new_population_size, new_elitism_size