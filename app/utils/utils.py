import yaml

def read_config(config_path="./config.yaml"):
# Load the YAML file
    with open(config_path) as file:
        data = yaml.safe_load(file)
    return data

