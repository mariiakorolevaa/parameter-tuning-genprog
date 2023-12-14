from scipy.optimize import differential_evolution, NonlinearConstraint

from fitness_functions import fitness_function
from json_edit import return_initial_json, get_json_file


def de_for_rational_scipy(path_to_repair, path_to_test, path_to_output, path_to_csv, acceleration_factor,
                          is_headless, n_jobs, pop_size, max_iter):
    if is_headless:
        bounds = [(0, 1), (0, 1)]  # Crossover rate, Mutation rate
    else:
        bounds = [(0, 1), (0, 1), (0, 1),
                  (0, 1)]  # Crossover rate, Mutation insertion rate, Mutation deletion rate, Mutation change rate

    original_json = get_json_file(is_headless)

    result = differential_evolution(fitness_function, bounds, args=(
        path_to_repair, path_to_test, path_to_output, path_to_csv, acceleration_factor, is_headless),
                                    strategy='best1bin', popsize=pop_size, maxiter=max_iter, tol=0.01,
                                    mutation=(0.5, 1), recombination=0.7,
                                    seed=None, callback=None, disp=False, polish=True, workers=n_jobs)

    # Get the best parameters
    best_params = result.x

    # Restore the original JSON
    return_initial_json(original_json, is_headless)

    return best_params


# Function defining the divisibility constraints:
# 1) Population size (x[0]) should be divisible by 4
# 2) Elitism size (x[1]) should be divisible by 2
def divisibility_constraint(x):
    return round(x[0]) % 4, round(x[1]) % 2


def de_for_integers_scipy(path_to_repair, path_to_test, path_to_output, path_to_csv, acceleration_factor, is_headless,
                          n_jobs, pop_size, max_iter):
    # Bounds for integer-encoded parameters
    bounds = [(4, 48), (2, 20)]

    nlc = NonlinearConstraint(fun=divisibility_constraint, lb=[0, 0], ub=[0, 0])

    original_json = get_json_file(is_headless)

    result = differential_evolution(fitness_function, bounds, args=(
        path_to_repair, path_to_test, path_to_output, path_to_csv, acceleration_factor, is_headless, False),
                                    strategy='best1bin', popsize=pop_size, maxiter=max_iter, tol=0.01,
                                    mutation=(0.5, 1), recombination=0.7,
                                    seed=None, callback=None, disp=False, polish=True, workers=n_jobs,
                                    constraints=nlc)

    # Get the best parameters
    best_params = result.x

    # Restore the original JSON
    return_initial_json(original_json, is_headless)

    return best_params