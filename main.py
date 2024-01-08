import argparse

from termcolor import colored
from tabulate import tabulate

from algorithm.de_scipy import de
from parameters.general_parameters import GeneralParameters
from algorithm.rs_scipy import rs


# Main function
def main(arguments):
    print("start")
    gen_params = GeneralParameters(arguments.path_to_repair,
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
                                   arguments.whisker_path)

    if arguments.mode == "rs":
        results = rs(gen_params)
        formatted_results = tabulate(results)
        print(colored('Results:', 'green', attrs=['bold']))
        print(formatted_results)
    elif arguments.mode == "de":
        results = de(gen_params)
        formatted_results = tabulate(results)
        print(colored('Results:', 'green', attrs=['bold']))
        print(formatted_results)

    else:
        print("Invalid arguments")


# Parameter parsing for the command line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Parameter tuning for Scratch program repair.")
    parser.add_argument("--is_rationals", action="store_true",
                        help="Use rational numbers for parameters")
    parser.add_argument("--mode", choices=["rs", "de"], default="rs", help="Optimization mode (random search or "
                                                                           "differential evolution)")
    parser.add_argument("--is_headless", default=True, action="store_true", help="Run in headless mode")
    parser.add_argument("--acceleration_factor", type=int, help="Acceleration factor")
    parser.add_argument("--path_to_repair", type=str,
                        help="Path to the scratch project to be "                                                                               "repaired")
    parser.add_argument("--path_to_test", type=str, help="Path to the file with the tests")
    parser.add_argument("--path_to_output", type=str, help="Path to the output folder")
    parser.add_argument("--path_to_csv", type=str, help="Path to the csv file")
    parser.add_argument("--path_to_config", type=str, help="Path to the config file")
    parser.add_argument("--whisker_path", type=str, help="Path to the whisker project folder")
    parser.add_argument("--population_size", type=int, help="Population size")
    parser.add_argument("--max_iter", type=int, help="Maximum number of iterations")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args)
