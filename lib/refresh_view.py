from __future__ import annotations
import os
import filecmp
import pandas as pd
from .connection import Connection


FILE_NAME = "Survey_updated_view.csv"
TEMP_NAME = "temp_view.csv"


def is_folder_empty(path_directory: str) -> bool:
    """
    Function designed to determine if a folder is empty

    Parameters
    ----------
    - path_directory: string of the path directory

    Return
    ------
    - boolean
    """
    if not os.path.isdir(path_directory):
        raise ValueError("Enter a valid folder path.\n")
    return not bool(os.listdir(path_directory))


def has_view_csv(path_directory: str) -> bool:
    """
    Function designed to determine if a view is already present in the folder

    Parameter
    ---------
    - path_directory: string of the path directory

    Return
    ------
    - boolean
    """
    if not os.path.isdir(path_directory):
        raise ValueError("Enter a valid folder path.\n")
    for file in os.listdir(path_directory):
        if file == FILE_NAME:
            return True


def is_view_updated(file_path_1: str, file_path_2: str) -> bool:
    """
    Function designed to determine if the generated view is different
    from the last one present in the folder.

    Parameters
    ----------
    - param file_path_1: string of the path files
    - param file_path_2: string of the path files

    Return
    ------
    - boolean
    """
    if not (os.path.isfile(file_path_1) & os.path.isfile(file_path_2)):
        raise ValueError("Check if the files path is correct\n")
    return not filecmp.cmp(file_path_1, file_path_2)


def trigger_sql_view_procedure(sql_procedure: str, db_connection: Connection) -> pd.DataFrame:
    """
    Function designed to return the view as a pandas DataFrame

    Parameters
    ----------
    - sql_procedure: string of the SQL procedure obtained using the get_all_data function
    - db_connection: Connection object to talk to the MSSQL Database server

    Return
    ------
    - pd.DataFrame
    """
    return pd.read_sql(sql_procedure, db_connection)


def database_view_refresh(sql_procedure: str, path_directory: str, db_connection: Connection) -> None:
    """
    Function designed to generate the view, save it immediately if folder is empty, if not check whether
    the view has been updated before saving it definitively.

    Parameters
    ----------
    - sql_procedure: string of the SQL procedure obtained using the get_all_data function
    - path_directory: string of the path directory
    - db_connection: Connection object to talk to the MSSQL Database server

    Return
    ------
    - None
    """
    current_view_path = os.path.join("Views", FILE_NAME)
    temp_view_path = os.path.join("Views", TEMP_NAME)

    if is_folder_empty(path_directory):
        trigger_sql_view_procedure(sql_procedure, db_connection).to_csv(path_or_buf=current_view_path, na_rep="-1")
        print("View saved\n")

    elif has_view_csv(path_directory):
        trigger_sql_view_procedure(sql_procedure, db_connection).to_csv(path_or_buf=temp_view_path, na_rep="-1")
        if is_view_updated(current_view_path, temp_view_path):
            os.remove(current_view_path)
            os.rename(temp_view_path, current_view_path)
            print("View has been updated.")
        else:
            os.remove(temp_view_path)
            print("Data is up to date. No update of the view.")
