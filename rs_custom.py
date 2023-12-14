import json
import random
from joblib import Parallel, delayed
from json_edit import return_initial_json, replace_json_values_for_rationals_headless, \
    replace_json_values_for_rationals_full, replace_json_values_for_integers, get_json_file
from run_project_cmd import run_cmd_and_get_tests, set_whisker_folder_path


# fitness function for simulated annealing algorithm
def fitness_function(passed_tests, total_tests):
    return passed_tests / total_tests


def random_search_for_rationals_one_iteration(path_to_repair, path_to_test, path_to_output, path_to_csv,
                                              acceleration_factor, initial_parameters, initial_fitness, is_headless,
                                              whisker_path):
    best_parameters = initial_parameters
    best_fitness = initial_fitness

    if is_headless:
        crossover_rate = random.uniform(0, 1)
        mutation_rate = random.uniform(0, 1)
        new_parameters = [crossover_rate, mutation_rate]
        replace_json_values_for_rationals_headless(crossover_rate, mutation_rate)

    else:
        crossover_rate = random.uniform(0, 1)
        mutation_insertion_rate = random.uniform(0, 1)
        mutation_deletion_rate = random.uniform(0, 1)
        mutation_change_rate = random.uniform(0, 1)
        new_parameters = [crossover_rate, mutation_insertion_rate, mutation_deletion_rate, mutation_change_rate]
        replace_json_values_for_rationals_full(crossover_rate, mutation_insertion_rate, mutation_deletion_rate,
                                               mutation_change_rate)

    set_whisker_folder_path(whisker_path)
    new_passed_tests, new_total_tests = run_cmd_and_get_tests(path_to_repair,
                                                              path_to_test,
                                                              path_to_output,
                                                              path_to_csv,
                                                              acceleration_factor, is_headless)

    new_fitness = fitness_function(new_passed_tests, new_total_tests)

    if new_fitness > best_fitness:
        best_parameters = new_parameters
        best_fitness = new_fitness

    return best_parameters, best_fitness


def random_search_for_rationals_parallel(path_to_repair, path_to_test, path_to_output, path_to_csv, acceleration_factor,
                                         n_jobs, is_headless):
    original_json = get_json_file(is_headless)
    results = Parallel(n_jobs=n_jobs)(
        delayed(random_search_for_rationals_one_iteration)(path_to_repair, path_to_test, path_to_output, path_to_csv,
                                                           acceleration_factor) for _ in range(n_jobs))
    return_initial_json(original_json, is_headless)

    return results


# one iteration of the random search
def random_search_for_integers_one_iteration(path_to_repair, path_to_test, path_to_output, path_to_csv,
                                             acceleration_factor, initial_parameters, initial_fitness):
    best_parameters = initial_parameters
    best_fitness = initial_fitness

    population_size = random.randint(1, 100)
    elitism_size = random.randint(1, population_size)
    new_parameters = [population_size, elitism_size]
    replace_json_values_for_integers(population_size, elitism_size, False)

    new_passed_tests, new_total_tests = run_cmd_and_get_tests(path_to_repair,
                                                              path_to_test,
                                                              path_to_output,
                                                              path_to_csv,
                                                              acceleration_factor, False)

    new_fitness = fitness_function(new_passed_tests, new_total_tests)

    if new_fitness > best_fitness:
        best_parameters = new_parameters
        best_fitness = new_fitness

    return best_parameters, best_fitness


# get the initial parameters and fitness by running the command with the default parameters
def run_initial_iteration(path_to_repair, path_to_test, path_to_output, path_to_csv, acceleration_factor, is_headless,
                          is_rational, whisker_path):
    initial_json = get_json_file(is_headless)
    # get the initial parameters from the json file
    json_data = json.load(initial_json)

    if is_headless and is_rational:
        initial_parameters = [json_data['crossover']['probability'],
                              json_data['mutation']['probability']]
    elif not is_headless and is_rational:
        initial_parameters = [json_data['crossover']['probability'],
                              json_data['mutation']['probability']['insertion'],
                              json_data['mutation']['probability']['deletion'],
                              json_data['mutation']['probability']['change']]
    else:
        initial_parameters = [json_data['algorithm']['populationSize'],
                              json_data['algorithm']['elitismSize']]

    # run the command in command line with the initial parameters
    set_whisker_folder_path(whisker_path)
    passed_tests, total_tests = run_cmd_and_get_tests(path_to_repair,
                                                      path_to_test,
                                                      path_to_output,
                                                      path_to_csv,
                                                      acceleration_factor, is_headless)
    fitness = fitness_function(passed_tests, total_tests)
    return initial_parameters, fitness


# random search for rational numbers in parallel mode
# args:
# path_to_repair: path to the scratch project to be repaired
# path_to_test: path to the file with the tests
# path_to_output: path to the output folder
# path_to_csv: path to the csv file
# acceleration_factor: acceleration factor (how many times faster the scratch project should run)
# n_jobs: number of parallel jobs
# is_headless: run in headless mode
def random_search_for_integers_parallel(path_to_repair, path_to_test, path_to_output, path_to_csv, acceleration_factor,
                                        n_jobs, is_headless):
    original_json = get_json_file(is_headless)
    results = Parallel(n_jobs=n_jobs)(
        delayed(random_search_for_integers_one_iteration)(path_to_repair, path_to_test, path_to_output, path_to_csv,
                                                          acceleration_factor) for _ in range(n_jobs))
    return_initial_json(original_json, is_headless)

    return results
