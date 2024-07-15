import yaml

def read_config(config_path="./config.yaml"):
    try:
        # Load the YAML file
        with open(config_path) as file:
            data = yaml.safe_load(file)
        return data
    except Exception as e:
        print("Exception in read_config",e)
        return None
