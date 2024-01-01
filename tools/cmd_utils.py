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
        df = pd.read_csv(path_to_csv)
    except pd.errors.EmptyDataError:
        return 1
    # remove all records where viable is false
    df = df[df.viable == True]
    # sort by fitness (descending) and time (ascending)
    df = df.sort_values(by=['fitness', 'time'], ascending=[False, True])
    # get the best fitness
    best_fitness = df.iloc[0]['fitness']

    return best_fitness
