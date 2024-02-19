import argparse
import json
import os
from tabulate import tabulate
from algorithm.de_scipy import de
from parameters.general_parameters import GeneralParameters
from algorithm.rs_scipy import rs
from tools.convert_txt_to_csv import transform_text_to_csv


def main(arguments):
    print("Starting...")
    gen_params = GeneralParameters(
        arguments.path_to_repair,
        arguments.path_to_test,
        arguments.path_to_output,
        arguments.path_to_csv,
        arguments.path_to_config,
        arguments.acceleration_factor,
        arguments.is_headless,
        arguments.is_float,
        1,
        arguments.max_iter,
        arguments.desired_fitness,
        arguments.whisker_path
    )
    current_directory = os.getcwd()
    if arguments.mode == "rs":
        results = rs(gen_params)
        # set directory as current directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        output_file_path_txt = "RS_all_results.txt"
        output_file_path_csv = "RS_all_results.csv"
    elif arguments.mode == "de":
        results = de(gen_params)
        output_file_path_txt = "DE_all_results.txt"
        output_file_path_csv = "DE_all_results.csv"
    else:
        print("Invalid mode specified.")
        return
    os.chdir(current_directory)
    transform_text_to_csv(output_file_path_txt, output_file_path_csv)
    print("Results written to " + output_file_path_csv)
    print(tabulate(results, headers="keys"))


def write_results_to_file(file_path, results):
    mode = 'a' if os.path.exists(file_path) else 'w'

    with open(file_path, mode) as file:
        if mode == 'a':
            file.write('\n\n')
        file.write(results)

    print(f"Results written to {file_path}")


def parse_args():
    with open('config.json', 'r') as f:
        config_data = json.load(f)

    return argparse.Namespace(
        is_float=config_data.get('is_float', False),
        mode=config_data.get('mode', 'rs'),
        is_headless=config_data.get('is_headless', True),
        acceleration_factor=config_data.get('acceleration_factor', None),
        path_to_repair=config_data.get('path_to_repair', None),
        path_to_test=config_data.get('path_to_test', None),
        path_to_output=config_data.get('path_to_output', None),
        path_to_csv=config_data.get('path_to_csv', None),
        path_to_config=config_data.get('path_to_config', None),
        whisker_path=config_data.get('whisker_path', None),
        max_iter=config_data.get('max_iter', 10),
        desired_fitness=config_data.get('desired_fitness', 0.00000001)
    )


if __name__ == "__main__":
    args = parse_args()
    main(args)
