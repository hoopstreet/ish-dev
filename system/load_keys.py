import os

def load_keys():
    env_path = "/root/.hoopstreet/creds/.env"

    if not os.path.exists(env_path):
        return

    with open(env_path) as f:
        for line in f:
            if "=" in line:
                k, v = line.strip().split("=", 1)
                os.environ[k] = v.strip('"').strip("'")
