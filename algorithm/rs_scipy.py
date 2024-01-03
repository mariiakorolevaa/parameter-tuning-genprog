import concurrent
import threading
from concurrent.futures import ThreadPoolExecutor

import numpy as np

from fitness.fitness_functions import fitness_function
from parameters.fitness_parameters import FitnessParameters
from parameters.general_parameters import GeneralParameters
from tools.stopping_condition import StoppingCondition


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
    futures = []
    results = []
    with ThreadPoolExecutor(max_workers=gen_parameters.n_jobs) as executor:
        for i in range(5):
            futures.append(executor.submit(run_optimization, gen_parameters))

        for future in concurrent.futures.as_completed(futures):
            rand_params, fitness_and_time = future.result()
            current_fitness = fitness_and_time[0]
            time = fitness_and_time[1]
            stopping_condition = StoppingCondition()
            results.append((rand_params, current_fitness))
            if stopping_condition.check_fitness_threshold(current_fitness):
                print("Stopping condition reached with fitness: ", current_fitness, " and parameters: ", rand_params)
                break

    sorted_results = sorted(results, key=lambda x: x[1])
    best_params = sorted_results[0][0]
    best_fitness = sorted_results[0][1]
    tabulate_results = [["best params", "best fitness"], [best_params, best_fitness]]
    return tabulate_results
