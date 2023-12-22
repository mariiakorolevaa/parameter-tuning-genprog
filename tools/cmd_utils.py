import os
import pandas as pd

from parameters.general_parameters import GeneralParameters


# run the command in command line
def run_command_to_repair(parameters: GeneralParameters):
    os.chdir(parameters.whisker_path)

    # delete csv file if it exists
    if os.path.exists(parameters.path_to_csv):
        os.remove(parameters.path_to_csv)

    command = "node servant repair -s " + parameters.path_to_repair + " -t " + parameters.path_to_test + \
              " -v " + parameters.path_to_csv + " -c " + parameters.path_to_config + " -o " + parameters.path_to_output + \
              " -a " + str(parameters.acceleration_factor) + " -k -l"
    if parameters.is_headless:
        command += " -d"

    os.system(command)


def run_cmd_and_get_fitness(parameters):
    run_command_to_repair(parameters)

    # process the csv file with the results
    df = pd.read_csv(parameters.path_to_csv)
    # remove all reconds where viable is false
    df = df[df.viable == True]
    if df.empty:
        return 1
    # sort by fitness (descending) and time (ascending)
    df = df.sort_values(by=['fitness', 'time'], ascending=[False, True])
    # get the best fitness
    best_fitness = df.iloc[0]['fitness']

    return best_fitness
