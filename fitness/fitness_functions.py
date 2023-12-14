from tools.json_utils import JsonUtils
from tools.run_cmd import run_cmd_and_get_tests


# Fitness function for the optimization
def fitness_function(parameters):
    json_utils = JsonUtils(parameters.general_parameters.json_path)
    if parameters.general_parameters.is_rationals:
        if parameters.general_parameters.is_headless:
            crossover_rate, mutation_rate = parameters.rand_params
            json_utils.replace_json_float_headless(crossover_rate, mutation_rate)
        else:

            if len(parameters.rand_parameters) == 2:
                crossover_rate, mutation_change_rate = parameters.rand_params
                mutation_insertion_rate = mutation_deletion_rate = 0
            else:
                crossover_rate, mutation_insertion_rate, mutation_deletion_rate, mutation_change_rate = parameters.rand_params

            json_utils.replace_json_float_full(crossover_rate,
                                               mutation_insertion_rate,
                                               mutation_deletion_rate,
                                               mutation_change_rate)

    else:
        population_size, elitism_size = parameters.rand_params
        population_size = round(population_size)
        elitism_size = round(elitism_size)
        json_utils.replace_json_int(population_size, elitism_size)

    passed_tests, total_tests = run_cmd_and_get_tests(parameters.general_parameters)

    return -passed_tests / total_tests  # use negative value for minimization
