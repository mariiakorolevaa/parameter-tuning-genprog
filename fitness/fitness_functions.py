import time

from parameters.fitness_parameters import FitnessParameters
from tools.json_files import JsonUtils
from tools.cmd import run_cmd_and_get_fitness

best_fitness = 1000000
stopping_criteria_reached = False
best_params = [0, 0, 0, 0]
time_for_best_params = 0
population_size = 0
elitism_size = 0
crossover_rate = 0
mutation_rate = 0
mutation_insertion_rate = 0
mutation_deletion_rate = 0
mutation_change_rate = 0
iteration = 0


def get_best_params():
    return best_params


def get_time_for_best_params():
    return time_for_best_params


def get_best_fitness():
    return best_fitness


def get_iteration():
    return iteration


# Fitness function for the optimization
def fitness_function(parameters: FitnessParameters):
    global best_fitness, best_params, population_size, \
        elitism_size, crossover_rate, mutation_rate, \
        mutation_insertion_rate, mutation_deletion_rate, mutation_change_rate, time_for_best_params

    json_utils = JsonUtils(parameters.general_parameters.path_to_config)
    if parameters.general_parameters.is_float:
        print("rationals mode")
        if parameters.general_parameters.is_headless:
            crossover_rate, mutation_rate = parameters.rand_params
            print("crossover_rate: ", crossover_rate)
            print("mutation_rate: ", mutation_rate)

            json_utils.replace_json_float_headless(crossover_rate, mutation_rate)
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

            json_utils.replace_json_float_full(crossover_rate,
                                               mutation_insertion_rate,
                                               mutation_deletion_rate,
                                               mutation_change_rate)

    else:
        print("integers mode")
        population_size, elitism_size = parameters.rand_params
        population_size = round(population_size)
        elitism_size = round(elitism_size)
        if population_size % 4 != 0 or elitism_size % 2 != 0:
            return best_fitness, time_for_best_params

        print("population_size: ", population_size)
        print("elitism_size: ", elitism_size)

        json_utils.replace_json_int(population_size, elitism_size)

    start_time = time.time()
    fitness, best_iteration, max_iteration = run_cmd_and_get_fitness(parameters.general_parameters)
    fitness = 1 / fitness
    end_time = time.time()
    exec_time = end_time - start_time
    if exec_time == 0:
        return best_fitness, time_for_best_params
    print("fitness: ", fitness)
    print("time: ", exec_time)
    if fitness < best_fitness:
        best_fitness = fitness
        if not parameters.general_parameters.is_float:
            best_params[0] = population_size
            best_params[1] = elitism_size
        elif parameters.general_parameters.is_headless and parameters.general_parameters.is_float:
            best_params[0] = crossover_rate
            best_params[1] = mutation_rate
        else:
            best_params[0] = crossover_rate
            best_params[1] = mutation_insertion_rate
            best_params[2] = mutation_deletion_rate
            best_params[3] = mutation_change_rate

        time_for_best_params = exec_time

    with open("/scratch/koroleva/parameter-tuning-genprog/RS_all_results.txt", "a") as f:
        f.write("max_iter: " + str(parameters.general_parameters.max_iter) + "\n")
        f.write("desired_fitness: " + str(parameters.general_parameters.desired_fitness) + "\n")
        if not parameters.general_parameters.is_float:
            f.write("population_size: " + str(population_size) + "\n")
            f.write("elitism_size: " + str(elitism_size) + "\n")

        elif parameters.general_parameters.is_headless and parameters.general_parameters.is_float:
            f.write("crossover_rate: " + str(crossover_rate) + "\n")
            f.write("mutation_rate: " + str(mutation_rate) + "\n")
        else:
            f.write("crossover_rate: " + str(crossover_rate) + "\n")
            f.write("mutation_insertion_rate: " + str(mutation_insertion_rate) + "\n")
            f.write("mutation_deletion_rate: " + str(mutation_deletion_rate) + "\n")
            f.write("mutation_change_rate: " + str(mutation_change_rate) + "\n")
        f.write("fitness: " + str(fitness) + "\n")
        f.write("best_fitness: " + str(best_fitness) + "\n")
        f.write("current iteration: " + str(iteration) + "\n")
        f.write("solution was found at: " + str(best_iteration) + " iteration\n")
        f.write("max number of iterations: " + str(max_iteration) + "\n")
        f.write("stopping_criteria_reached: " + str(stopping_criteria_reached) + "\n")

        f.write("time: " + str(exec_time) + "\n")
        f.write("\n")
    return fitness, exec_time


def fitness_function_de(x, *args):
    global best_fitness, best_params, population_size, \
        elitism_size, crossover_rate, mutation_rate, \
        mutation_insertion_rate, mutation_deletion_rate, mutation_change_rate, time_for_best_params, \
        iteration

    global stopping_criteria_reached

    if stopping_criteria_reached:
        return best_fitness
    parameters = args[0]
    json_utils = JsonUtils(parameters.general_parameters.path_to_config)

    if parameters.general_parameters.is_float:
        print("rationals mode")
        if parameters.general_parameters.is_headless:
            print("headless mode, number of parameters: ", len(x))
            crossover_rate, mutation_rate = x
            print("crossover_rate: ", crossover_rate)
            print("mutation_rate: ", mutation_rate)

            json_utils.replace_json_float_headless(crossover_rate, mutation_rate)
        else:
            print("full mode, number of parameters: ", len(x))
            crossover_rate, mutation_insertion_rate, mutation_deletion_rate, mutation_change_rate = x
            print("crossover_rate: ", crossover_rate)
            print("mutation_insertion_rate: ", mutation_insertion_rate)
            print("mutation_deletion_rate: ", mutation_deletion_rate)
            print("mutation_change_rate: ", mutation_change_rate)

            json_utils.replace_json_float_full(crossover_rate,
                                               mutation_insertion_rate,
                                               mutation_deletion_rate,
                                               mutation_change_rate)

    else:
        print("integers mode")
        if len(x) == 1:
            population_size, = x
            elitism_size = best_params[1]  # Use the existing value for elitism_size
        else:
            population_size, elitism_size = x
        population_size = round_pop_size(population_size)
        elitism_size = round_el_size(elitism_size)
        if population_size % 4 != 0 or elitism_size % 2 != 0:
            return best_fitness

        print("population_size: ", population_size)
        print("elitism_size: ", elitism_size)

        json_utils.replace_json_int(population_size, elitism_size)

    iteration += 1
    start_time = time.time()
    fitness, best_iteration, max_iteration  = run_cmd_and_get_fitness(parameters.general_parameters)
    fitness = 1 / fitness
    end_time = time.time()
    exec_time = end_time - start_time
    if fitness < best_fitness:
        best_fitness = fitness
        if not parameters.general_parameters.is_float:
            best_params[0] = population_size
            best_params[1] = elitism_size
        elif parameters.general_parameters.is_headless and parameters.general_parameters.is_float:
            best_params[0] = crossover_rate
            best_params[1] = mutation_rate
        else:
            best_params[0] = crossover_rate
            best_params[1] = mutation_insertion_rate
            best_params[2] = mutation_deletion_rate
            best_params[3] = mutation_change_rate

        time_for_best_params = exec_time
    print("fitness: ", fitness)
    print("best_fitness: ", best_fitness)
    print("current iteration: ", iteration)
    if best_fitness <= parameters.general_parameters.desired_fitness or iteration >= parameters.general_parameters.max_iter:
        stopping_criteria_reached = True
        print("stopping criteria reached")

    with open("/scratch/koroleva/parameter-tuning-genprog/DE_all_results.txt", "a") as f:
        f.write("max_iter: " + str(parameters.general_parameters.max_iter) + "\n")
        f.write("desired_fitness: " + str(parameters.general_parameters.desired_fitness) + "\n")

        if not parameters.general_parameters.is_float:
            f.write("population_size: " + str(population_size) + "\n")
            f.write("elitism_size: " + str(elitism_size) + "\n")

        elif parameters.general_parameters.is_headless and parameters.general_parameters.is_float:
            f.write("crossover_rate: " + str(crossover_rate) + "\n")
            f.write("mutation_rate: " + str(mutation_rate) + "\n")
        else:
            f.write("crossover_rate: " + str(crossover_rate) + "\n")
            f.write("mutation_insertion_rate: " + str(mutation_insertion_rate) + "\n")
            f.write("mutation_deletion_rate: " + str(mutation_deletion_rate) + "\n")
            f.write("mutation_change_rate: " + str(mutation_change_rate) + "\n")
        f.write("fitness: " + str(fitness) + "\n")
        f.write("best_fitness: " + str(best_fitness) + "\n")
        f.write("current step: " + str(iteration) + "\n")
        f.write("solution was found at: " + str(best_iteration) + " iteration\n")
        f.write("max number of iterations: " + str(max_iteration) + "\n")
        f.write("stopping_criteria_reached: " + str(stopping_criteria_reached) + "\n")

        f.write("time: " + str(exec_time) + "\n")
        f.write("\n")
    return fitness


def stopping_criteria(xk, convergence):
    print("stopping_criteria_function called")
    global stopping_criteria_reached
    if stopping_criteria_reached:
        if len(xk) == 2:
            xk[0] = best_params[0]
            xk[1] = best_params[1]
        else:
            xk[0] = best_params[0]
            xk[1] = best_params[1]
            xk[2] = best_params[2]
            xk[3] = best_params[3]

        print("stopping_criteria_function returning True")
        return True
    print("stopping_criteria_function returning False")
    return False


# Round the population size to the nearest valid value
def round_pop_size(pop_size):
    valid_values = list(range(12, 50, 4))
    return min(valid_values, key=lambda x: abs(x - pop_size))


# Round the elitism size to the nearest valid value
def round_el_size(el_size):
    valid_values = list(range(2, 10, 2))
    return min(valid_values, key=lambda x: abs(x - el_size))
