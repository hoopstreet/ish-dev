def classify(error):
    e = error.lower()

    if "not found" in e:
        return "missing_dependency"
    if "permission denied" in e:
        return "permission"
    if "syntax error" in e:
        return "syntax"
    if "command not found" in e:
        return "missing_command"
    return "unknown"
