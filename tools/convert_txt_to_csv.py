import pandas as pd


def transform_text_to_csv(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    data = []
    temp_dict = {}
    for line in lines:
        if line.strip() and ':' in line:
            key, value = line.strip().split(': ')
            temp_dict[key] = value
        elif temp_dict:
            data.append(temp_dict)
            temp_dict = {}

    if temp_dict:
        data.append(temp_dict)

    df = pd.DataFrame(data)

    column_mapping = {
        'max_iter': 'Max Iterations',
        'desired_fitness': 'Desired Fitness',
        'population_size': 'Population Size',
        'elitism_size': 'Elitism Size',
        'fitness': 'Fitness',
        'best_fitness': 'Best Fitness',
        'current iteration': 'Current Iteration',
        'solution was found at': 'Solution Found At',
        'max number of iterations': 'Max Iterations Found',
        'stopping_criteria_reached': 'Stopping Criteria Reached',
        'time': 'Time'
    }

    df = df.rename(columns=column_mapping)

    df.to_csv(output_file, index=False)