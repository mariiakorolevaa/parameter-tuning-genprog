class GeneralParameters:

    def __init__(self, path_to_repair, path_to_test, path_to_output, path_to_csv, path_to_config, acceleration_factor,
                 is_headless, is_float, n_jobs, max_iter, desired_fitness, whisker_path):
        self.path_to_repair = path_to_repair
        self.path_to_test = path_to_test
        self.path_to_output = path_to_output
        self.path_to_csv = path_to_csv
        self.path_to_config = path_to_config
        self.acceleration_factor = acceleration_factor
        self.is_headless = is_headless
        self.is_float = is_float
        self.n_jobs = n_jobs
        self.max_iter = max_iter
        self.desired_fitness = desired_fitness
        self.whisker_path = whisker_path
