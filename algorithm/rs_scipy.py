import numpy as np
from joblib import Parallel, delayed
from scipy.optimize import minimize

from fitness.fitness_functions import fitness_function
from fitness.fitness_parameters import FitnessParameters
from tools.json_utils import JsonUtils
from tools.utils import generate_valid_population_and_elitism


def callable_function(rand_params, gen_parameters):
    return fitness_function(parameters=FitnessParameters(rand_params, gen_parameters))


# Random Search for rational numbers using SciPy
def rs_float(parameters):
    if parameters.is_headless:
        # Crossover rate, Mutation rate
        bounds = [(0, 1), (0, 1)]
    else:
        # Crossover rate, Mutation insertion rate, Mutation deletion rate, Mutation change rate
        bounds = [(0, 1), (0, 1), (0, 1), (0, 1)]

    json_utils = JsonUtils(parameters.json_path)
    original_json = json_utils.get_json_file()

    initial_values = [np.random.rand(len(bounds)) for _ in range(parameters.n_jobs)]

    results = Parallel(n_jobs=parameters.n_jobs)(
        delayed(minimize)(callable_function, x0=(init_vals, parameters), bounds=bounds, method='L-BFGS-B') for init_vals
        in initial_values)
    best_params_list = [result.x for result in results]
    json_utils.return_initial_json(original_json, parameters.is_headless)
    return best_params_list


# Random Search for integers using SciPy
def rs_int(parameters):
    bounds = ((4, 48), (2, 20),)
    population_size_bounds = (4, 48)
    elitism_size_bounds = (2, 20)

    json_utils = JsonUtils(parameters.json_path)
    original_json = json_utils.get_json_file()

    # Generate initial values using the custom function
    initial_population_size, initial_elitism_size = generate_valid_population_and_elitism(population_size_bounds,
                                                                                          elitism_size_bounds)
    initial_values = [np.random.randint(low=low, high=high) for low, high in bounds]
    initial_values[0] = initial_population_size
    initial_values[1] = initial_elitism_size

    results = Parallel(n_jobs=parameters.n_jobs)(
        delayed(minimize)(callable_function,
                          x0=init_vals,
                          args=(parameters,),
                          bounds=[population_size_bounds, elitism_size_bounds],
                          method='L-BFGS-B')
        for init_vals in [initial_values]
    )
    best_params_list = [result.x for result in results]
    json_utils.return_initial_json(original_json, parameters.is_headless)
    return best_params_list
