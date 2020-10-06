from __future__ import annotations
from cryptography.fernet import Fernet
from getpass import getpass


class PasswordEncryption:
    """
    Create a PasswordEncryption object.

    Attributes
    ----------
    - key: bytes, cryptographic symmetric key to encrypt database password.
    Value is set by invoking the setter method generate_password_key(self)

    - encrypted_password: bytes, encrypted password using the Fernet symmetric
    key invoking the setter method password_encryption()
    """

    def __init__(self) -> None:
        self.key = None
        self.encrypted_password = None

    def generate_password_key(self) -> PasswordEncryption:
        """
        Setter method that create a symmetric key (bytes) and assign it
        to the attribute key

        Return
        ------
        - PasswordEncryption
        """
        key = Fernet.generate_key()
        self.key = Fernet(key)
        return self

    def password_encryption(self) -> None:
        """
        Setter method that asks the user for his password in order
        to encrypt it and set the encryption message as value to the
        attribute encrypted_password

        Return
        ------
        - None
        """
        password = getpass(prompt="Enter your mssql password:\n")
        self.encrypted_password = self.key.encrypt(password.encode("utf-8"))

    def decrypting_password(self, key: bytes, encrypted_password: bytes) -> str:
        """
        Method defined to decrypt encrypted passwords to pass it into the
        database connection string.

        parameter
        ---------
        - key: bytes generated using the Fernet algorithm
        - encrypted_password: bytes-encrypted password

        Return
        ------
        - str
        """
        return self.key.decrypt(self.encrypted_password).decode("utf-8")
