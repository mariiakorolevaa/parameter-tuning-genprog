import os

import numpy as np
from joblib import Parallel, delayed

from fitness.fitness_functions import fitness_function
from parameters.fitness_parameters import FitnessParameters
from parameters.general_parameters import GeneralParameters


def rs(gen_parameters: GeneralParameters):
    # if csv file is not exist, create it

    n_iterations = 20

    results = parallel_random_search(n_iterations, gen_parameters.n_jobs, gen_parameters)

    for result in results:
        print(result)


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


def run_optimization(gen_parameters: GeneralParameters):
    if gen_parameters.is_rationals:
        rand_params = generate_random_parameters_float(gen_parameters.is_headless)
    else:
        rand_params = generate_random_parameters_int()
    fitness_parameters = FitnessParameters(rand_parameters=rand_params, general_parameters=gen_parameters)
    fitness = fitness_function(parameters=fitness_parameters)
    return rand_params, fitness


def parallel_random_search(n_iterations, n_jobs, gen_parameters: GeneralParameters):
    results = Parallel(n_jobs=n_jobs)(delayed(run_optimization)(gen_parameters) for _ in range(n_iterations))

    results.sort(key=lambda x: x[1], reverse=True)

    best_params = results[0]
    best_fitness = best_params[1]
    print("best fitness: ", best_fitness)
    print("best params: ", best_params)

    return best_params
