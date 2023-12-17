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
              " -v " + parameters.path_to_csv + " -o " + parameters.path_to_output + \
              " -a " + str(parameters.acceleration_factor) + " -k -l"
    if parameters.is_headless:
        command += " -d"

    os.system(command)


def run_cmd_and_get_tests(parameters):
    run_command_to_repair(parameters)

    # process the csv file with the results
    df = pd.read_csv(parameters.path_to_csv)
    # get line from the table where viable value is true
    viable_row = df.loc[df['viable']]
    if viable_row.empty:
        return 0, 0
    # get the number of passed tests and total tests
    passed_tests = viable_row['numPass'].values[0]
    total_tests = viable_row['numFail'].values[0]

    return passed_tests, total_tests
