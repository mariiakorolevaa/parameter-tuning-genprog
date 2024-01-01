from parameters.fitness_parameters import FitnessParameters
from tools.json_utils import JsonUtils
from tools.cmd_utils import run_cmd_and_get_fitness

best_fitness = 1
stopping_criteria_reached = False
best_params = [0, 0, 0, 0]
population_size = 0
elitism_size = 0
crossover_rate = 0
mutation_rate = 0
mutation_insertion_rate = 0
mutation_deletion_rate = 0
mutation_change_rate = 0


def get_best_params():
    return best_params


# Fitness function for the optimization
def fitness_function(parameters: FitnessParameters):
    global best_fitness, best_params, population_size, \
        elitism_size, crossover_rate, mutation_rate, \
        mutation_insertion_rate, mutation_deletion_rate, mutation_change_rate

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
        if population_size % 4 != 0 or elitism_size % 2 != 0:
            return best_fitness

        print("population_size: ", population_size)
        print("elitism_size: ", elitism_size)

        copy_path = json_utils.replace_json_int(population_size, elitism_size)

    fitness = run_cmd_and_get_fitness(parameters.general_parameters, copy_path)

    current_fitness = 1 / fitness
    if current_fitness < best_fitness:
        best_fitness = current_fitness
        if not parameters.general_parameters.is_rationals:
            best_params[0] = population_size
            best_params[1] = elitism_size
        elif parameters.general_parameters.is_headless and parameters.general_parameters.is_rationals:
            best_params[0] = crossover_rate
            best_params[1] = mutation_rate
        else:
            best_params[0] = crossover_rate
            best_params[1] = mutation_insertion_rate
            best_params[2] = mutation_deletion_rate
            best_params[3] = mutation_change_rate

    return current_fitness


def fitness_function_de(x, *args):
    global best_fitness, population_size, elitism_size, best_params, \
        crossover_rate, mutation_rate, mutation_insertion_rate, \
        mutation_deletion_rate, mutation_change_rate
    parameters = args[0]
    json_utils = JsonUtils(parameters.general_parameters.path_to_config)

    if parameters.general_parameters.is_rationals:
        if parameters.general_parameters.is_headless:
            crossover_rate, mutation_rate = x
            copy_path = json_utils.replace_json_float_headless(crossover_rate, mutation_rate)
        else:
            crossover_rate, mutation_insertion_rate, mutation_deletion_rate, mutation_change_rate = x
            copy_path = json_utils.replace_json_float_full(crossover_rate,
                                                           mutation_insertion_rate,
                                                           mutation_deletion_rate,
                                                           mutation_change_rate)
    else:
        population_size, elitism_size = x
        population_size = round(population_size)
        elitism_size = round(elitism_size)
        if population_size % 4 != 0 or elitism_size % 2 != 0:
            return best_fitness
        copy_path = json_utils.replace_json_int(population_size, elitism_size)

    fitness = run_cmd_and_get_fitness(parameters.general_parameters, copy_path)
    current_fitness = 1 / fitness

    if current_fitness < best_fitness:
        best_fitness = current_fitness
        if not parameters.general_parameters.is_rationals:
            best_params[0] = population_size
            best_params[1] = elitism_size
        elif parameters.general_parameters.is_headless and parameters.general_parameters.is_rationals:
            best_params[0] = crossover_rate
            best_params[1] = mutation_rate
        else:
            best_params[0] = crossover_rate
            best_params[1] = mutation_insertion_rate
            best_params[2] = mutation_deletion_rate
            best_params[3] = mutation_change_rate

    if best_fitness < 0.12:
        global stopping_criteria_reached
        stopping_criteria_reached = True

    return current_fitness


def stopping_criteria(xk, convergence):
    if stopping_criteria_reached:
        if len(xk) == 2:
            xk[0] = best_params[0]
            xk[1] = best_params[1]
        else:
            xk[0] = best_params[0]
            xk[1] = best_params[1]
            xk[2] = best_params[2]
            xk[3] = best_params[3]

        return True
