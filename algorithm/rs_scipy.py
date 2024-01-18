import time

import numpy as np
import time as tme

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
    message = ""
    best_fitness = 1
    best_params = []
    time_for_best_params = 0
    start_time = tme.time()
    end_time = start_time
    iteration = 0

    for i in range(gen_parameters.max_iter):
        iteration += 1
        rand_params, fitness_and_time = run_optimization(gen_parameters)
        fitness = fitness_and_time[0]
        exec_time = fitness_and_time[1]
        if fitness < best_fitness:
            best_fitness = fitness
            best_params = rand_params
            time_for_best_params = exec_time
            if gen_parameters.desired_fitness >= best_fitness:
                message = "Desired fitness reached in iteration " + str(iteration)
                end_time = time.time()
                break

    if iteration >= gen_parameters.max_iter:
        end_time = tme.time()
        message = "Maximum number of iterations reached"

    formatted_time = tme.strftime("%H:%M:%S", tme.gmtime(end_time - start_time))
    tabulate_results = [["ALGORITHM", "best params", "best fitness", "time", "search time", "result"],
                        ["RS", best_params, best_fitness, time_for_best_params, formatted_time, message]]
    return tabulate_results
