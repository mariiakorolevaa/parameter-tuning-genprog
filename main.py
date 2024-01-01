import argparse

from algorithm.de_scipy import de
from parameters.general_parameters import GeneralParameters
from algorithm.rs_scipy import rs

# For testing
path_to_repair = "C:/Users/kiris/Documents/GitHub/scratch-repair-study-dataset/0-toy-examples/repair-subjects/Max-1.sb3"
path_to_test = "C:/Users/kiris/Documents/GitHub/scratch-repair-study-dataset/0-toy-examples/tests/Max-manual.js"
path_to_csv = "C:/Users/kiris/Documents/GitHub/output_repair/result.csv"
path_to_output = "C:/Users/kiris/Documents/GitHub/output_repair/"
whisker_folder_path = "C:/Users/kiris/WebstormProjects/whisker-main/"
path_to_config = "C:/Users/kiris/WebstormProjects/whisker-main/config/repair/genProg-headless-chicken.json"
acceleration_factor = 10
n_jobs = 2
mode = "rs"
is_headless = True
is_rationals = True


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
                                   arguments.n_jobs,
                                   10,
                                   0,
                                   arguments.whisker_path)

    if arguments.mode == "rs":
        results = rs(gen_params)
        print(results)

    elif arguments.mode == "de":
        results = de(gen_params)
        print("results: ", results)

    else:
        print("Invalid arguments")


# Parameter parsing for the command line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Parameter tuning for Scratch program repair.")
    parser.add_argument("--is_rationals", default=is_rationals, action="store_true",
                        help="Use rational numbers for parameters")
    parser.add_argument("--mode", choices=["rs", "de"], default=mode, help="Optimization mode (random search or "
                                                                           "differential evolution)")
    parser.add_argument("--n_jobs", type=int, default=n_jobs, help="Number of parallel jobs")
    parser.add_argument("--is_headless", default=is_headless, action="store_true", help="Run in headless mode")
    parser.add_argument("--acceleration_factor", type=int, default=acceleration_factor, help="Acceleration factor")
    parser.add_argument("--path_to_repair", default=path_to_repair, type=str, help="Path to the scratch project to be "                                                                               "repaired")
    parser.add_argument("--path_to_test", default=path_to_test, type=str, help="Path to the file with the tests")
    parser.add_argument("--path_to_output", default=path_to_output, type=str, help="Path to the output folder")
    parser.add_argument("--path_to_csv", default=path_to_csv, type=str, help="Path to the csv file")
    parser.add_argument("--path_to_config", default=path_to_config, type=str, help="Path to the config file")
    parser.add_argument("--whisker_path", default=whisker_folder_path, type=str, help="Path to the whisker project folder")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args)
