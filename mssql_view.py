def get_view() -> None:
    db_user_name: str = input(
        "Enter your user name. Use 'sa' if your are the admin.\n"
           )
    db_password: PasswordEncryption = PasswordEncryption()
    db_password.generate_password_key().password_encryption()
    db_password: str = db_password.decrypting_password(
        db_password.key,
        db_password.encrypted_password
        )
    # Error capture for DB connection
    try:
        mssql: Connection = Connection(
            "ODBC Driver 17 for SQL Server",
            "localhost",
            "Survey_Sample_A18",
            db_user_name,
            db_password
            ).connect()
    except pyodbc.Error as error_message:
        print("Error: " + error_message.args[1])
        return

    procedure: str = get_all_data_survey(mssql.connection)
    database_view_refresh(procedure, "Views", mssql.connection)
    mssql.disconnect()


if __name__ == '__main__':
    from lib.missing_pkg import are_missing_dependencies
    if are_missing_dependencies():
        print(" *======= Installation of missing dependencies. *=======\n")
        import sys
        import subprocess
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', '-e', '.']
            )
    print("\n")
    from lib.connection import Connection
    from lib.encryption import PasswordEncryption
    from lib.get_all_data import get_all_data_survey
    from lib.refresh_view import database_view_refresh
    import pyodbc
    get_view()
