import os
import subprocess

import pandas as pd

from parameters.general_parameters import GeneralParameters

evaluation_type = "merge"
is_best_iteration_mode = True


# evaluation_type = "average"

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
        experiments_path = parameters.path_to_csv
        experiment_folders = [folder for folder in os.listdir(experiments_path) if
                              os.path.isdir(os.path.join(experiments_path, folder))]
        merged_data = pd.DataFrame()
        for folder in experiment_folders:
            folder_path = os.path.join(experiments_path, folder)
            file_path = os.path.join(folder_path, "output.csv")
            if os.path.exists(file_path):
                data = pd.read_csv(file_path)
                merged_data = pd.concat([merged_data, data], ignore_index=True)
        output_path = os.path.join(experiments_path, "output_merged.csv")
        merged_data.to_csv(output_path, index=False)
        df = pd.read_csv(output_path, converters={'viable': lambda x: True if x == 'true' else False})
    except Exception as e:
        print(e)
        return 1

    best_fitness, hash_code = get_best_fitness(df)
    best_iteration, max_iteration = get_iteration(df, hash_code)
    print("best iteration: ", best_iteration)

    return int(best_fitness), best_iteration, max_iteration


def get_best_fitness(df):
    df = df[df['iteration'] == df['iteration'].max()]
    df = df.sort_values(by=['fitness'], ascending=[False])
    fitness_column = df['fitness']
    hashcode_column = df['hashCode']
    best_fitness = 1
    best_hashcode = None
    for i in range(len(fitness_column)):
        if fitness_column.iloc[i] != "fitness":
            best_fitness = fitness_column.iloc[i]
            best_hashcode = hashcode_column.iloc[i]
            break

    return int(best_fitness), best_hashcode


def get_average(fitness_list):
    average_fitness = 0
    for fitness in fitness_list:
        average_fitness += fitness

    average_fitness /= len(fitness_list)

    return average_fitness


def get_iteration(df, hash_code):
    best_iteration = None
    max_iteration = df['iteration'].max()
    for index, row in df.iterrows():
        if row['hashCode'] == hash_code:
            best_iteration = int(row['iteration'])
            break
    return best_iteration, max_iteration
