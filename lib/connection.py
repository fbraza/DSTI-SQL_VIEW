from __future__ import annotations
import pyodbc


class Connection:
    """
    Create a unique connection object using a singleton design pattern.
    At instantiation __new__(cls, *args, **kwargs) is invoked to check
    if an instance has already been created checking the class variable
    instance.

    Attributes
    ----------
    - connection_string: string that hold the necessary details to connect
    to the database.
    - connection: pyodbc.Connection object (see pyodbc documentation).
    Use the setter method connect() to set its value.
    """
    instance = None

    def __new__(cls, *args, **kwargs) -> Connection:
        if cls.instance is None:
            cls.instance = object.__new__(Connection)
        return cls.instance

    def __init__(self, driver: str, server: str, db_name: str,
                 uid: str, pwd: str) -> None:
        self.connection_string = "DRIVER={};SERVER={};DATABASE={};UID={};PWD={}".format(driver, server, db_name, uid, pwd)
        self.connection = None

    def connect(self) -> Connection:
        """
        Setter method to set the value of the attribute:: connection to
        a pyodbc.Connection object. Method can be chained.

        Return
        ------
        - Connection
        """
        self.connection = pyodbc.connect(self.connection_string)
        return self

    def disconnect(self) -> None:
        """
        Setter method used to close database connection. The connection
        attribute and class variable Connection.instance are set to None.
        Output a disconnection message.

        Return
        ------
        - None
        """
        self.connection.close()
        self.connection = None
        Connection.instance = None
        print("Disconnecting from Database.\n")
