import argparse
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
        arguments.is_rationals,
        1,
        arguments.population_size,
        arguments.max_iter,
        arguments.desired_fitness,
        arguments.whisker_path
    )

    if arguments.mode == "rs":
        results = rs(gen_params)
        formatted_results = tabulate(results)

        output_file_path_txt = "RS-results.txt"
        output_file_path_csv = "RS-results.csv"
    elif arguments.mode == "de":
        results = de(gen_params)
        formatted_results = tabulate(results)

        output_file_path_txt = "DE-results.txt"
        output_file_path_csv = "DE-results.csv"
    else:
        print("Invalid mode specified.")
        return

    write_results_to_file(output_file_path_txt, formatted_results)
    transform_text_to_csv(output_file_path_txt, output_file_path_csv)
    print("Done.")


def write_results_to_file(file_path, results):
    mode = 'a' if os.path.exists(file_path) else 'w'

    with open(file_path, mode) as file:
        if mode == 'a':
            file.write('\n\n')
        file.write(results)

    print(f"Results written to {file_path}")


def parse_args():
    parser = argparse.ArgumentParser(description="Parameter tuning for Scratch program repair.")
    parser.add_argument("--is_rationals", action="store_true", help="Use rational numbers for parameters")
    parser.add_argument("--mode", choices=["rs", "de"], default="rs",
                        help="Optimization mode (random search or differential evolution)")
    parser.add_argument("--is_headless", default=True, action="store_true", help="Run in headless mode")
    parser.add_argument("--acceleration_factor", type=int, help="Acceleration factor")
    parser.add_argument("--path_to_repair", type=str, help="Path to the scratch project to be repaired")
    parser.add_argument("--path_to_test", type=str, help="Path to the file with the tests")
    parser.add_argument("--path_to_output", type=str, help="Path to the output folder")
    parser.add_argument("--path_to_csv", type=str, help="Path to the csv file")
    parser.add_argument("--path_to_config", type=str, help="Path to the config file")
    parser.add_argument("--whisker_path", type=str, help="Path to the whisker project folder")
    parser.add_argument("--population_size", type=int, help="Population size")
    parser.add_argument("--max_iter", type=int, default=10, help="Maximum number of iterations")
    parser.add_argument("--desired_fitness", default=271, type=float, help="Desired fitness")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args)
