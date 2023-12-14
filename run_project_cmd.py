import os
import pandas as pd

desired_folder_path = "C:/Users/kiris/WebstormProjects/whisker-main/"


def set_whisker_folder_path(path):
    global desired_folder_path
    desired_folder_path = path


# run the command in command line
def run_command_to_repair(path_to_repair, path_to_test, path_to_output, path_to_csv, acceleration_factor, is_headless):
    os.chdir(desired_folder_path)
    if is_headless:
        command = "node servant repair -s " + path_to_repair + " -t " + path_to_test + \
                  " -v " + path_to_csv + " -o " + path_to_output + " -a " + str(acceleration_factor) + " -d -k -l"
    else:
        command = "node servant repair -s " + path_to_repair + " -t " + path_to_test + \
                  " -v " + path_to_csv + " -o " + path_to_output + " -a " + str(acceleration_factor) + " -k -l"
    os.system(command)


def run_cmd_and_get_tests(path_to_repair, path_to_test, path_to_output, path_to_csv, acceleration_factor, is_headless):
    run_command_to_repair(path_to_repair, path_to_test, path_to_output, path_to_csv, acceleration_factor, is_headless)

    # process the csv file with the results
    df = pd.read_csv(path_to_csv)
    # get line from the table where viable value is true
    viable_row = df.loc[df['viable'] == True]
    if viable_row.empty:
        return 0, 0
    # get the number of passed tests and total tests
    passed_tests = viable_row['numPass'].values[0]
    total_tests = viable_row['numFail'].values[0]

    return passed_tests, total_tests
