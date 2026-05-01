#!/usr/bin/env python3
import os

def load_keys():
    env_paths = [
        "/root/.hoopstreet/creds/.env",
        os.path.expanduser("~/.hoopstreet/creds/.env")
    ]

    for path in env_paths:
        try:
            if os.path.exists(path):
                with open(path) as f:
                    for line in f:
                        if "=" in line:
                            k, v = line.strip().split("=", 1)
                            os.environ[k] = v.strip('"')
        except:
            pass

load_keys()
