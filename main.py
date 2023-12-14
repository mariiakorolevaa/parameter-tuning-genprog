import argparse

from algorithm.de_scipy import de_int, de_float
from general_parameters import GeneralParameters
from algorithm.rs_scipy import rs_int, rs_float

# For testing
path_to_repair = "C:/Users/kiris/Documents/GitHub/scratch-repair-study-dataset/0-toy-examples/repair-subjects/Max-1.sb3"
path_to_test = "C:/Users/kiris/Documents/GitHub/scratch-repair-study-dataset/0-toy-examples/tests/Max-manual.js"
path_to_csv = "C:/Users/kiris/Documents/GitHub/output_repair/result.csv"
path_to_output = "C:/Users/kiris/Documents/GitHub/output_repair/"
json_path_full = "C:/Users/kiris/WebstormProjects/whisker-main/config/repair/genProg.json"
json_path_headless = "C:/Users/kiris/WebstormProjects/whisker-main/config/repair/genProg-headless-chicken.json"
whisker_folder_path = "C:/Users/kiris/WebstormProjects/whisker-main/"
acceleration_factor = "10"


# Main function
def main(arguments):
    print("start")
    if arguments.is_headless:
        json_path = json_path_headless
    else:
        json_path = json_path_full
    gen_params = GeneralParameters(arguments.path_to_repair,
                                   arguments.path_to_test,
                                   arguments.path_to_output,
                                   arguments.path_to_csv,
                                   arguments.acceleration_factor,
                                   arguments.is_headless,
                                   arguments.is_rationals,
                                   arguments.n_jobs,
                                   10,
                                   0,
                                   arguments.whisker_path,
                                   json_path)

    if arguments.mode == "rs" and arguments.is_rationals:
        results = rs_float(gen_params)
        print(results)

    elif arguments.mode == "rs" and not arguments.is_rationals:
        results = rs_int(gen_params)
        print("results: ", results)

    elif arguments.mode == "de" and arguments.is_rationals:
        results = de_float(gen_params)
        print("results: ", results)

    elif arguments.mode == "de" and not arguments.is_rationals:
        results = de_int(gen_params)
        print("results: ", results)

    else:
        print("Invalid arguments")


# Parameter parsing for the command line arguments
# Options:
# --is_rationals: optimize the parameters represented as rational numbers or integers
# --mode: optimization mode (random search or differential evolution)
# --n_jobs: number of parallel jobs
# --is_headless: run in headless mode
def parse_args():
    parser = argparse.ArgumentParser(description="Parameter tuning for Scratch program repair.")
    parser.add_argument("--is_rationals", default=False, action="store_true",
                        help="Use rational numbers for parameters")
    parser.add_argument("--mode", choices=["rs", "de"], default="rs", help="Optimization mode (random search or "
                                                                           "differential evolution)")
    parser.add_argument("--n_jobs", type=int, default=4, help="Number of parallel jobs")
    parser.add_argument("--is_headless", default=False, action="store_true", help="Run in headless mode")
    parser.add_argument("--acceleration_factor", type=int, default=10, help="Acceleration factor")
    parser.add_argument("--path_to_repair", default=path_to_repair, type=str, help="Path to the scratch project to be "
                                                                                   "repaired")
    parser.add_argument("--path_to_test", default=path_to_test, type=str, help="Path to the file with the tests")
    parser.add_argument("--path_to_output", default=path_to_output, type=str, help="Path to the output folder")
    parser.add_argument("--path_to_csv", default=path_to_csv, type=str, help="Path to the csv file")
    parser.add_argument("--json_path_full", default=json_path_full, type=str, help="Path to the json file with full "
                                                                                   "parameters")
    parser.add_argument("--json_path_headless", default=json_path_headless, type=str, help="Path to the json file with "
                                                                                           "headless parameters")
    parser.add_argument("--whisker_path", default=whisker_folder_path, type=str, help="Path to the whisker project "
                                                                                      "folder")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args)
