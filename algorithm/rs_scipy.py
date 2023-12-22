import numpy as np
from scipy import optimize

from fitness.fitness_functions import callable_function
from parameters.fitness_parameters import FitnessParameters
from tools.generation_utils import generate_valid_population_and_elitism


# Random Search for rational numbers using SciPy
def rs_float(gen_parameters):
    if gen_parameters.is_headless:
        # Crossover rate, Mutation rate
        b = [(0, 1), (0, 1)]
    else:
        # Crossover rate, Mutation insertion rate, Mutation deletion rate, Mutation change rate
        b = [(0, 1), (0, 1), (0, 1), (0, 1)]

    initial_values = np.random.rand(len(b))

    x = initial_values
    args = FitnessParameters(rand_parameters=x, general_parameters=gen_parameters)

    results = maximize_function([callable_function, x, b, args])

    best_params_list = results.x

    return best_params_list


# Random Search for integers using SciPy
def rs_int(gen_parameters):
    b = ((4, 48), (2, 20),)
    population_size_bounds = (4, 48)
    elitism_size_bounds = (2, 20)

    # Generate initial values using the custom function
    initial_population_size, initial_elitism_size = generate_valid_population_and_elitism(population_size_bounds,
                                                                                          elitism_size_bounds)
    x = [initial_population_size, initial_elitism_size]
    args = FitnessParameters(rand_parameters=x, general_parameters=gen_parameters)

    results = maximize_function([callable_function, x, b, args])

    best_params_list = results.x

    return best_params_list


def maximize_function(args):
    f, x, b, a = args
    result = optimize.minimize(fun=f, x0=x, args=a, method='BFGS', jac=False, bounds=b)
    return result

