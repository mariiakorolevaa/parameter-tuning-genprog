import numpy as np
from scipy import optimize

from fitness.fitness_functions import callable_function
from fitness.fitness_parameters import FitnessParameters
from tools.json_utils import JsonUtils
from tools.utils import generate_valid_population_and_elitism


# Random Search for rational numbers using SciPy
def rs_float(gen_parameters):
    if gen_parameters.is_headless:
        # Crossover rate, Mutation rate
        b = [(0, 1), (0, 1)]
    else:
        # Crossover rate, Mutation insertion rate, Mutation deletion rate, Mutation change rate
        b = [(0, 1), (0, 1), (0, 1), (0, 1)]

    json_utils = JsonUtils(gen_parameters.json_path)
    original_json = json_utils.get_json_file()

    initial_values = np.random.rand(len(b))

    x = initial_values
    args = FitnessParameters(rand_parameters=x, general_parameters=gen_parameters)

    results = minimize_function([callable_function, x, b, args])

    best_params_list = [result.x for result in results]

    json_utils.return_initial_json(original_json, gen_parameters.is_headless)
    return best_params_list


# Random Search for integers using SciPy
def rs_int(gen_parameters):
    b = ((4, 48), (2, 20),)
    population_size_bounds = (4, 48)
    elitism_size_bounds = (2, 20)

    json_utils = JsonUtils(gen_parameters.json_path)
    original_json = json_utils.get_json_file()

    # Generate initial values using the custom function
    initial_population_size, initial_elitism_size = generate_valid_population_and_elitism(population_size_bounds,
                                                                                          elitism_size_bounds)
    x = [initial_population_size, initial_elitism_size]
    args = FitnessParameters(rand_parameters=x, general_parameters=gen_parameters)

    results = minimize_function([callable_function, x, b, args])

    best_params_list = [result.x for result in results]
    json_utils.return_initial_json(original_json, gen_parameters.is_headless)
    return best_params_list


def minimize_function(args):
    f, x, b, a = args
    result = optimize.minimize(fun=f, x0=x, args=a, method='BFGS', jac=True, bounds=b)
    return result

