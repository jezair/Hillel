GLOBAL_CONFIG = {"feature_a": True, "max_retries": 3}

class Configuration:
    def __init__(self, updates, validator=None):
        self.updates = updates
        self.validator = validator
        self.original = GLOBAL_CONFIG.copy()

    def __enter__(self):
        GLOBAL_CONFIG.update(self.updates)
        if self.validator and not self.validator(GLOBAL_CONFIG):
            raise ValueError("Invalid configuration")


    def __exit__(self, exc_type, exc_value, traceback):
        GLOBAL_CONFIG.clear()
        GLOBAL_CONFIG.update(self.original)

def validate_config(config):
    # Ensure max_retries >= 0
    return config.get("max_retries", 0) >= 0

# === TEST ===
print(f"BASE: {GLOBAL_CONFIG}\n")

try:
    with Configuration({"max_retries": 5}, validator=validate_config):
        print("\nAll right:", GLOBAL_CONFIG)
except ValueError as e:
    print("\nValidate error:", e)

print("\nNOW:", GLOBAL_CONFIG)

# ====

try:
    with Configuration({"max_retries": -2}, validator=validate_config):
        print("\nAll right:", GLOBAL_CONFIG)
except ValueError as e:
    print("\nValidate error:", e)

print("NOW:", GLOBAL_CONFIG)