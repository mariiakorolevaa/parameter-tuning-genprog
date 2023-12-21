import json


class JsonUtils:
    def __init__(self, json_path):
        self.json_path = json_path

    def get_json_file(self):
        with open(self.json_path, "r") as file:
            original_content = file.read()
        return original_content

    # TODO How to pass as parameter the path to config json file?
    def replace_json_float_headless(self, crossover_rate, mutation_rate):
        with open(self.json_path, "r") as file:
            original_content = file.read()

        with open(self.json_path, "r") as file:
            json_data = json.load(file)
        json_data['algorithm']['populationSize'] = 4
        json_data['stoppingCondition']['conditions'][1]['iterations'] = 10
        json_data['stoppingCondition']['conditions'][2]['duration'] = 10000
        json_data['mutation']['probability'] = mutation_rate
        json_data['crossover']['probability'] = crossover_rate

        with open(self.json_path, "w") as file:
            json.dump(json_data, file, indent=2)

        return original_content

    # TODO How to pass as parameter the path to config json file?
    def replace_json_float_full(self, crossover_rate, mutation_insert_rate, mutation_delete_rate,
                                mutation_change_rate):
        with open(self.json_path, "r") as file:
            original_content = file.read()

        with open(self.json_path, "r") as file:
            json_data = json.load(file)

        json_data['algorithm']['populationSize'] = 4
        json_data['stoppingCondition']['conditions'][1]['duration'] = 10000
        json_data['mutation']['probability']['insertion'] = mutation_insert_rate
        json_data['mutation']['probability']['deletion'] = mutation_delete_rate
        json_data['mutation']['probability']['change'] = mutation_change_rate
        json_data['crossover']['probability'] = crossover_rate

        with open(self.json_path, "w") as file:
            json.dump(json_data, file, indent=2)

        return original_content

    # TODO How to pass as parameter the path to config json file?
    def replace_json_int(self, population_size, elitism_size):
        with open(self.json_path, "r") as file:
            original_content = file.read()

        with open(self.json_path, "r") as file:
            json_data = json.load(file)
        json_data['algorithm']['populationSize'] = population_size
        json_data['algorithm']['elitismSize'] = elitism_size

        with open(self.json_path, "w") as file:
            json.dump(json_data, file, indent=2)

        return original_content

    # return the json file to its initial state
    def return_initial_json(self, original_file, is_headless):
        with open(self.json_path, "w") as file:
            file.write(original_file)

