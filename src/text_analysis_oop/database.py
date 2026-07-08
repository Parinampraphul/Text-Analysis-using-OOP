from dataclasses import dataclass

import pyodbc

from .security import hash_password, verify_password


@dataclass(frozen=True)
class User:
    id: int
    name: str
    email: str


class DatabaseConnectionError(RuntimeError):
    pass


class UserRepository:
    def __init__(self, connection_string: str) -> None:
        try:
            self.connection = pyodbc.connect(connection_string)
        except pyodbc.Error as exc:
            raise DatabaseConnectionError(
                "Could not connect to SQL Server. Check SQLSERVER_SERVER, "
                "SQLSERVER_DATABASE, SQLSERVER_TRUSTED_CONNECTION, "
                "SQLSERVER_USERNAME, and SQLSERVER_PASSWORD in your .env file."
            ) from exc
        self.create_tables()

    def create_tables(self) -> None:
        cursor = self.connection.cursor()
        cursor.execute(
            """
            IF OBJECT_ID('dbo.users', 'U') IS NULL
            BEGIN
                CREATE TABLE dbo.users (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    name NVARCHAR(255) NOT NULL,
                    email NVARCHAR(255) NOT NULL UNIQUE,
                    password_hash NVARCHAR(512) NOT NULL
                )
            END
            """
        )
        self.connection.commit()

    def create_user(self, name: str, email: str, password: str) -> User:
        normalized_name = name.strip()
        normalized_email = email.strip().lower()
        cursor = self.connection.cursor()
        cursor.execute(
            """
            INSERT INTO dbo.users (name, email, password_hash)
            OUTPUT INSERTED.id
            VALUES (?, ?, ?)
            """,
            normalized_name,
            normalized_email,
            hash_password(password),
        )
        user_id = cursor.fetchone()[0]
        self.connection.commit()
        return User(id=user_id, name=normalized_name, email=normalized_email)

    def email_exists(self, email: str) -> bool:
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT 1 FROM dbo.users WHERE email = ?",
            email.strip().lower(),
        )
        return cursor.fetchone() is not None

    def authenticate(self, email: str, password: str) -> User | None:
        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT id, name, email, password_hash
            FROM dbo.users
            WHERE email = ?
            """,
            email.strip().lower(),
        )
        row = cursor.fetchone()

        if row is None or not verify_password(password, row.password_hash):
            return None

        return User(id=row.id, name=row.name, email=row.email)

    def close(self) -> None:
        self.connection.close()
