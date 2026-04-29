#!/usr/bin/env python3
import sys

def analyze(log):
    if "not found" in log:
        return "Missing package or command"
    if "permission denied" in log:
        return "Permission issue"
    if "network error" in log:
        return "Network/repo issue"
    return "Unknown error"

if __name__ == "__main__":
    data = sys.stdin.read()
    print("DEBUG:", analyze(data))
