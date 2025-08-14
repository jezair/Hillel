GLOBAL_CONFIG = {"feature_a": True, "max_retries": У}

def validate_config(config):
    return config.get("max_retries", 0) >= 0

validate_config(GLOBAL_CONFIG)