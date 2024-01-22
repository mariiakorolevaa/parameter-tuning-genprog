import os
import subprocess

import pandas as pd

from parameters.general_parameters import GeneralParameters

evaluation_type = "average"


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

    if evaluation_type == "merge":
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

        best_fitness = sort_by_fitness(df)

    else:
        try:
            fitness_list = []
            experiments_path = parameters.path_to_csv
            experiment_folders = [folder for folder in os.listdir(experiments_path) if
                                  os.path.isdir(os.path.join(experiments_path, folder))]
            for folder in experiment_folders:
                folder_path = os.path.join(experiments_path, folder)
                file_path = os.path.join(folder_path, "output.csv")
                if os.path.exists(file_path):
                    f = sort_by_fitness(pd.read_csv(file_path))
                    fitness_list.append(f)

            best_fitness = get_average(fitness_list)
            print("average fitness: ", best_fitness)
        except Exception as e:
            print(e)
            return 1

    return int(best_fitness)


def sort_by_fitness(df):
    df = df[df['iteration'] == df['iteration'].max()]
    df = df.sort_values(by=['fitness'], ascending=[False])
    fitness_column = df['fitness']
    best_fitness = 1
    for i in range(len(fitness_column)):
        if fitness_column.iloc[i] != "fitness":
            best_fitness = fitness_column.iloc[i]
            break

    return int(best_fitness)


def get_average(fitness_list):
    average_fitness = 0
    for fitness in fitness_list:
        average_fitness += fitness

    average_fitness /= len(fitness_list)

    return average_fitness
