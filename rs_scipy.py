import numpy as np
from joblib import Parallel, delayed
from scipy.optimize import minimize

from fitness_functions import fitness_function
from json_edit import return_initial_json, get_json_file
from utils import generate_valid_population_and_elitism


# Random Search for rational numbers using SciPy
def rs_for_rationals_scipy(path_to_repair, path_to_test, path_to_output, path_to_csv, acceleration_factor,
                           n_jobs, is_headless):
    if is_headless:
        bounds = [(0, 1), (0, 1)]  # Crossover rate, Mutation rate
    else:
        bounds = [(0, 1), (0, 1), (0, 1),
                  (0, 1)]  # Crossover rate, Mutation insertion rate, Mutation deletion rate, Mutation change rate

    original_json = get_json_file(is_headless)

    def objective(params):
        return fitness_function(params, path_to_repair, path_to_test, path_to_output, path_to_csv, acceleration_factor,
                                is_headless, True)

    initial_values = [np.random.rand(len(bounds)) for _ in range(n_jobs)]
    results = Parallel(n_jobs=n_jobs)(
        delayed(minimize)(objective, x0=init_vals, bounds=bounds, method='L-BFGS-B') for init_vals in initial_values)
    best_params_list = [result.x for result in results]
    return_initial_json(original_json, is_headless)
    return best_params_list


# Random Search for integers using SciPy
def rs_for_integers_scipy(path_to_repair, path_to_test, path_to_output, path_to_csv, acceleration_factor,
                          n_jobs, is_headless):
    bounds = ((4, 48), (2, 20),)
    population_size_bounds = (4, 48)
    elitism_size_bounds = (2, 20)
    original_json = get_json_file(is_headless)

    def objective(params):
        return fitness_function(params, path_to_repair, path_to_test, path_to_output, path_to_csv, acceleration_factor,
                                is_headless, False)

    # Generate initial values using the custom function
    initial_population_size, initial_elitism_size = generate_valid_population_and_elitism(population_size_bounds,
                                                                                          elitism_size_bounds)
    initial_values = [np.random.randint(low=low, high=high) for low, high in bounds]
    initial_values[0] = initial_population_size
    initial_values[1] = initial_elitism_size

    results = Parallel(n_jobs=n_jobs)(
        delayed(minimize)(objective, x0=init_vals, bounds=[population_size_bounds, elitism_size_bounds],
                          method='L-BFGS-B')
        for init_vals in [initial_values]
    )
    best_params_list = [result.x for result in results]
    return_initial_json(original_json, is_headless)
    return best_params_list
