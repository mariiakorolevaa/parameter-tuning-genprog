from parameters.fitness_parameters import FitnessParameters
from tools.json_utils import JsonUtils
from tools.cmd_utils import run_cmd_and_get_fitness


# Fitness function for the optimization
def fitness_function(parameters: FitnessParameters):
    json_utils = JsonUtils(parameters.general_parameters.path_to_config)
    if parameters.general_parameters.is_rationals:
        print("rationals mode")
        if parameters.general_parameters.is_headless:
            print("headless mode, number of parameters: ", len(parameters.rand_params))
            crossover_rate, mutation_rate = parameters.rand_params
            print("crossover_rate: ", crossover_rate)
            print("mutation_rate: ", mutation_rate)

            copy_path = json_utils.replace_json_float_headless(crossover_rate, mutation_rate)
        else:
            print("full mode, number of parameters: ", len(parameters.rand_params))
            if len(parameters.rand_params) == 2:
                crossover_rate, mutation_change_rate = parameters.rand_params
                mutation_insertion_rate = mutation_deletion_rate = 0
            else:
                crossover_rate, mutation_insertion_rate, mutation_deletion_rate, mutation_change_rate = parameters.rand_params
                print("crossover_rate: ", crossover_rate)
                print("mutation_insertion_rate: ", mutation_insertion_rate)
                print("mutation_deletion_rate: ", mutation_deletion_rate)
                print("mutation_change_rate: ", mutation_change_rate)

            copy_path = json_utils.replace_json_float_full(crossover_rate,
                                                           mutation_insertion_rate,
                                                           mutation_deletion_rate,
                                                           mutation_change_rate)

    else:
        print("integers mode")
        population_size, elitism_size = parameters.rand_params
        population_size = round(population_size)
        elitism_size = round(elitism_size)
        if population_size % 4 != 0:
            return 0
        if elitism_size % 2 != 0:
            return 0
        print("population_size: ", population_size)
        print("elitism_size: ", elitism_size)

        copy_path = json_utils.replace_json_int(population_size, elitism_size)

    fitness = run_cmd_and_get_fitness(parameters.general_parameters, copy_path)

    return 1 / fitness


# To use in scipy algorithms
def callable_function(x, args: FitnessParameters):
    return fitness_function(parameters=args)
