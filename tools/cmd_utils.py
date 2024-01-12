import os
import subprocess

import pandas as pd

from parameters.general_parameters import GeneralParameters


# run the command in command line
def run_command_to_repair(parameters: GeneralParameters):
    os.chdir(parameters.whisker_path)

    command = "./prepare_experiment.py settings/repair.ini"
    subprocess.run(command, shell=True, check=True)

    command = "./1_submit_cluster_job.sh"
    subprocess.run(command, shell=True, check=True)

    command = "python utils/collect_results.py -r results/"
    subprocess.run(command, shell=True, check=True)


def run_cmd_and_get_fitness(parameters):
    run_command_to_repair(parameters)

    try:
        # Указать путь к папке с экспериментами
        experiments_path = "/scratch/koroleva/whisker-cluster-experiments/results"

        # Get a list of all folders in the experiments path
        experiment_folders = [folder for folder in os.listdir(experiments_path) if
                              os.path.isdir(os.path.join(experiments_path, folder))]

        merged_data = pd.DataFrame()

        # Iterate over all folders of experiments
        for folder in experiment_folders:
            folder_path = os.path.join(experiments_path, folder)

            # Check if the output file exists
            file_path = os.path.join(folder_path, "output.csv")
            if os.path.exists(file_path):
                data = pd.read_csv(file_path)
                merged_data = merged_data.append(data, ignore_index=True)

        # Save the merged data to a csv file
        output_path = os.path.join(experiments_path, "output_merged.csv")
        merged_data.to_csv(output_path, index=False)
        print("Merged data saved to: ", output_path)
        df = pd.read_csv(output_path, converters={'viable': lambda x: True if x == 'true' else False})
        print("Merge data read from: ", output_path)
    except Exception as e:
        print(e)
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
