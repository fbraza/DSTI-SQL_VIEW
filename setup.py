from setuptools import setup


setup(
    name="mssql_view",
    version="1.0",
    py_modules=["mssql_view"],
    install_requires=["pyodbc", "pandas", "cryptography"]
        )
