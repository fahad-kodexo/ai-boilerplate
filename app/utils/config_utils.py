import yaml


def read_config(config_path="./config.yaml"):
    try:
        # Load the YAML file
        with open(config_path) as file:
            return yaml.safe_load(file)
    except Exception as e:
        print("Exception in read_config", e)
        return None
