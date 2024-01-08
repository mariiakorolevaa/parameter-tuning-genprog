import os

import pandas as pd

from parameters.general_parameters import GeneralParameters


# run the command in command line
def run_command_to_repair(parameters: GeneralParameters):
    os.chdir(parameters.whisker_path)

    command = "./prepare_experiment.py settings/repair.ini"
    os.system(command)

    command = "./1_submit_cluster_job.sh"
    os.system(command)

    command = "python utils/collect_results.py -r results/"
    os.system(command)


def run_cmd_and_get_fitness(parameters):
    run_command_to_repair(parameters)

    # process the csv file with the results
    try:
        df = pd.read_csv("results/result.csv", converters={'viable': lambda x: True if x == 'true' else False})
    except pd.errors.EmptyDataError:
        return 1
    # remove all records where viable is false
    # sort by fitness (descending) and time (ascending)
    df = df.sort_values(by=['fitness', 'time'], ascending=[False, True])
    fitness_column = df['fitness']
    time_column = df['time']
    best_fitness = 1
    time = 0
    for i in range(len(fitness_column)):
        if fitness_column.iloc[i] != "fitness":
            best_fitness = fitness_column.iloc[i]
            break

    for i in range(len(time_column)):
        if time_column.iloc[i] != "time":
            time = time_column.iloc[i]
            break

    return int(best_fitness), int(time)
