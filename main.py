import argparse

from de_scipy import de_for_integers_scipy, de_for_rational_scipy
from json_edit import set_json_paths
from rs_scipy import rs_for_integers_scipy, rs_for_rationals_scipy

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
    if arguments.mode == "rs" and arguments.is_rationals:
        results = rs_for_rationals_scipy(arguments.path_to_repair,
                                         arguments.path_to_test,
                                         arguments.path_to_output,
                                         arguments.path_to_csv,
                                         arguments.acceleration_factor,
                                         arguments.n_jobs,
                                         arguments.is_headless)
        print(results)

    elif arguments.mode == "rs" and not arguments.is_rationals:
        results = rs_for_integers_scipy(arguments.path_to_repair,
                                        arguments.path_to_test,
                                        arguments.path_to_output,
                                        arguments.path_to_csv,
                                        arguments.acceleration_factor,
                                        arguments.n_jobs,
                                        arguments.is_headless)
        print("results: ", results)

    elif arguments.mode == "de" and arguments.is_rationals:
        max_iter = 10
        if (arguments.json_path_full != json_path_full) or (arguments.json_path_headless != json_path_headless):
            set_json_paths(arguments.json_path_full, arguments.json_path_headless)

        results = de_for_rational_scipy(arguments.path_to_repair,
                                        arguments.path_to_test,
                                        arguments.path_to_output,
                                        arguments.path_to_csv,
                                        arguments.acceleration_factor,
                                        arguments.is_headless,
                                        arguments.n_jobs,
                                        pop_size=10,
                                        max_iter=max_iter)
        print("results: ", results)

    elif arguments.mode == "de" and not arguments.is_rationals:
        max_iter = 10
        if (arguments.json_path_full != json_path_full) or (arguments.json_path_headless != json_path_headless):
            set_json_paths(arguments.json_path_full, arguments.json_path_headless)

        results = de_for_integers_scipy(arguments.path_to_repair,
                                        arguments.path_to_test,
                                        arguments.path_to_output,
                                        arguments.path_to_csv,
                                        arguments.acceleration_factor,
                                        arguments.is_headless,
                                        arguments.n_jobs,
                                        pop_size=10,
                                        max_iter=max_iter)
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
    parser.add_argument("--mode", choices=["rs", "de"], default="de", help="Optimization mode (random search or "
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
