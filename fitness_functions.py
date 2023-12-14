from json_edit import replace_json_values_for_integers, replace_json_values_for_rationals_full, \
    replace_json_values_for_rationals_headless
from run_project_cmd import run_cmd_and_get_tests


# Fitness function for the optimization
def fitness_function(params, path_to_repair, path_to_test, path_to_output, path_to_csv, acceleration_factor,
                     is_headless, is_rationals):
    if is_rationals:
        if is_headless:
            crossover_rate, mutation_rate = params
            replace_json_values_for_rationals_headless(crossover_rate, mutation_rate)
        else:

            if len(params) == 2:
                crossover_rate, mutation_change_rate = params
                mutation_insertion_rate = mutation_deletion_rate = 0
            else:
                crossover_rate, mutation_insertion_rate, mutation_deletion_rate, mutation_change_rate = params

            replace_json_values_for_rationals_full(crossover_rate, mutation_insertion_rate, mutation_deletion_rate,
                                                   mutation_change_rate)

    else:
        population_size, elitism_size = params
        population_size = round(population_size)
        elitism_size = round(elitism_size)
        replace_json_values_for_integers(population_size, elitism_size, is_headless)

    passed_tests, total_tests = run_cmd_and_get_tests(path_to_repair, path_to_test, path_to_output, path_to_csv,
                                                      acceleration_factor, is_headless)

    return -passed_tests / total_tests  # use negative value for minimization