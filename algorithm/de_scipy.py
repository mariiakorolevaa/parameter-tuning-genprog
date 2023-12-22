import numpy as np
from scipy.optimize import differential_evolution, NonlinearConstraint

from fitness.fitness_functions import callable_function
from parameters.fitness_parameters import FitnessParameters
from tools.generation_utils import generate_valid_population_and_elitism
from tools.json_utils import JsonUtils


def de_float(gen_parameters):
    if gen_parameters.is_headless:
        # Crossover rate, Mutation rate
        bounds = [(0, 1), (0, 1)]
        mutation_rate = 0.5
        crossover_rate = 0.7
        initial_values = [crossover_rate, mutation_rate]
    else:
        # Crossover rate, Mutation insertion rate, Mutation deletion rate, Mutation change rate
        bounds = [(0, 1), (0, 1), (0, 1), (0, 1)]
        mutation_insert_rate = 0.3333
        mutation_delete_rate = 0.3333
        mutation_change_rate = 0.3333
        crossover_rate = 0.7
        initial_values = [crossover_rate, mutation_insert_rate, mutation_delete_rate, mutation_change_rate]

    json_utils = JsonUtils(gen_parameters.path_to_config)
    original_json = json_utils.get_json_file()

    fitness_parameters = FitnessParameters(rand_parameters=initial_values, general_parameters=gen_parameters)
    result = differential_evolution(callable_function, bounds,
                                    args=(fitness_parameters,),
                                    strategy='best1bin',
                                    popsize=gen_parameters.pop_size,
                                    maxiter=gen_parameters.max_iter,
                                    tol=0.01,
                                    mutation=(0.5, 1),
                                    recombination=0.7,
                                    seed=None,
                                    callback=None,
                                    disp=False,
                                    polish=True,
                                    workers=gen_parameters.n_jobs)

    # Get the best parameters
    best_params = result.x

    # Restore the original JSON
    json_utils.return_initial_json(original_json, gen_parameters.is_headless)

    return best_params


# Function defining the divisibility constraints:
# 1) Population size (x[0]) should be divisible by 4
# 2) Elitism size (x[1]) should be divisible by 2
def divisibility_constraint(x):
    return round(x[0]) % 4, round(x[1]) % 2


def de_int(gen_parameters):
    # Bounds for integer-encoded parameters
    b = [(12, 48), (2, 8)]

    nlc = NonlinearConstraint(fun=divisibility_constraint, lb=[0, 0], ub=[0, 0])
    population_size_bounds = (12, 48)
    elitism_size_bounds = (2, 8)

    json_utils = JsonUtils(gen_parameters.path_to_config)
    original_json = json_utils.get_json_file()

    # Generate initial values using the custom function
    initial_population_size, initial_elitism_size = generate_valid_population_and_elitism(population_size_bounds,
                                                                                          elitism_size_bounds)
    x = [initial_population_size, initial_elitism_size]
    args = FitnessParameters(rand_parameters=x, general_parameters=gen_parameters)

    result = differential_evolution(callable_function, bounds=b,
                                    x0=x,
                                    args=(args,),
                                    strategy='best1bin',
                                    tol=0.01,
                                    mutation=(0.5, 1),
                                    recombination=0.7,
                                    seed=None, callback=None,
                                    disp=False, polish=True,
                                    workers=gen_parameters.n_jobs,
                                    constraints=nlc)

    # Get the best parameters
    best_params = result.x

    # Restore the original JSON
    json_utils.return_initial_json(original_json, gen_parameters.is_headless)

    return best_params
