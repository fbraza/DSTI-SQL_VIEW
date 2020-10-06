def are_missing_dependencies():
    """
    Function that returns true if missing dependencies are found

    Return
    ------
    - None
    """
    import pkg_resources
    required = {"pandas", "cryptography", "pyodbc"}
    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = required - installed
    return bool(missing)
