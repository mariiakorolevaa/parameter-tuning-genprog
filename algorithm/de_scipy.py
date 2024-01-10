import time

import numpy as np
from scipy.optimize import differential_evolution

from fitness.fitness_functions import fitness_function_de, stopping_criteria, get_best_params, get_time_for_best_params, \
    get_iteration
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


def de(gen_parameters: GeneralParameters):
    if gen_parameters.is_rationals:
        if gen_parameters.is_headless:
            bounds = [(0, 1), (0, 1)]
        else:
            bounds = [(0, 1), (0, 1), (0, 1), (0, 1)]
    else:
        bounds = [(8, 17), (2, 4)]
    rand_params = generate_random_parameters_int() if not gen_parameters.is_rationals else generate_random_parameters_float(
        gen_parameters.is_headless)
    fitness_parameters = FitnessParameters(rand_parameters=rand_params, general_parameters=gen_parameters)

    start_time = time.time()
    end_time = start_time

    result = differential_evolution(
        func=fitness_function_de,
        bounds=bounds,
        args=(fitness_parameters,),
        strategy='best1bin',
        tol=0.12,
        mutation=(0.5, 1),
        recombination=0.7,
        seed=None,
        disp=False,
        maxiter=gen_parameters.max_iter,
        popsize=10,
        workers=1,
        callback=stopping_criteria
    )
    stop_time = time.time()
    iteration = get_iteration()

    best_params = get_best_params()
    # get as many elements as there are parameters
    if gen_parameters.is_rationals:
        if gen_parameters.is_headless:
            best_params = best_params[:2]
        else:
            best_params = best_params[:4]
    else:
        best_params = best_params[:2]
    best_fitness = result.fun

    print("best fitness: ", best_fitness)
    print("best params: ", best_params)
    print("time for best params: ", get_time_for_best_params())

    if iteration >= gen_parameters.max_iter:
        end_time = time.time()
        message = "Maximum number of iterations reached"
    else:
        message = "Desired fitness reached in iteration " + str(iteration)

    # time in format hh:mm:ss
    formatted_time = time.strftime("%H:%M:%S", time.gmtime(end_time - start_time))
    tabulate_results = [["best params", "best fitness", "time", "search time", "result"],
                        [best_params, 1 / best_fitness, formatted_time, message]]

    tabulate_results = [["best params", "best fitness"], [best_params, best_fitness]]
    return tabulate_results
