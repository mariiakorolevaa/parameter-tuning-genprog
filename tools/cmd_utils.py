import os
from datetime import datetime

import pandas as pd

from parameters.general_parameters import GeneralParameters


# run the command in command line
def run_command_to_repair(parameters: GeneralParameters, copy_path, path_to_csv):
    os.chdir(parameters.whisker_path)

    command = "node servant repair -s " + parameters.path_to_repair + " -t " + parameters.path_to_test + \
              " -v " + path_to_csv + " -c " + copy_path + " -o " + parameters.path_to_output + \
              " -a " + str(parameters.acceleration_factor)
    if parameters.is_headless:
        command += " -d"

    os.system(command)


def run_cmd_and_get_fitness(parameters, copy_path):
    path_to_csv = parameters.path_to_csv.replace(".csv",
                                                 f"_{os.getpid()}_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv")
    run_command_to_repair(parameters, copy_path, path_to_csv)

    # process the csv file with the results
    try:
        df = pd.read_csv(path_to_csv, converters={'viable': lambda x: True if x == 'true' else False})
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
