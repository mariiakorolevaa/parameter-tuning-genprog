import numpy as np

from fitness.fitness_functions import fitness_function
from parameters.fitness_parameters import FitnessParameters
from parameters.general_parameters import GeneralParameters


def generate_random_parameters_int():
    population_size = np.random.randint(12, 49)
    population_size -= population_size % 4
    elitism_size = np.random.randint(2, 9)
    elitism_size -= elitism_size % 2
    return [population_size, elitism_size]


def generate_random_parameters_float(is_headless: bool):
    if is_headless:
        crossover_rate = np.random.uniform(0, 1)
        mutation_rate = np.random.uniform(0, 1)
        return [crossover_rate, mutation_rate]
    else:
        crossover_rate = np.random.uniform(0, 1)
        mutation_insert_rate = np.random.uniform(0, 1)
        mutation_delete_rate = np.random.uniform(0, 1)
        mutation_change_rate = np.random.uniform(0, 1)
        return [crossover_rate, mutation_insert_rate, mutation_delete_rate, mutation_change_rate]


def run_optimization(gen_parameters):
    if gen_parameters.is_rationals:
        rand_params = generate_random_parameters_float(gen_parameters.is_headless)
    else:
        rand_params = generate_random_parameters_int()

    fitness_parameters = FitnessParameters(rand_params, gen_parameters)
    fitness_and_time = fitness_function(fitness_parameters)

    return rand_params, fitness_and_time


def rs(gen_parameters: GeneralParameters):
    best_fitness = 1
    best_params = []
    time_for_best_params = 0

    for i in range(gen_parameters.max_iter):
        rand_params, fitness_and_time = run_optimization(gen_parameters)
        fitness = fitness_and_time[0]
        time = fitness_and_time[1]
        if fitness < best_fitness:
            best_fitness = fitness
            best_params = rand_params
            time_for_best_params = time

    tabulate_results = [["best params", "best fitness", "time"], [best_params, best_fitness, time_for_best_params]]
    return tabulate_results
