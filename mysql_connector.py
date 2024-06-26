import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()


class MySQLConnector:
    # __cursor:sqlite3.Cursor

    def __init__(self, host: str = 'localhost', user: str = 'root', password: str = os.getenv('mysql_password'), db_name: str = 'hw_6_db'):
        self.__connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.__cursor = self.__connection.cursor()
        # self.__cursor.execute(f"CREATE DATABASE {db_name}; ")
        self.__cursor.execute(f"USE {db_name};")

    @property
    def cursor(self):
        return self.__cursor

    def exec(self, query: str):
        return self.__cursor.execute(query)

    def commit(self):
        self.__connection.commit()

    def __del__(self):
        self.__cursor.close()
        self.__connection.close()


def create_table_user():
    con = MySQLConnector()

    con.cursor.execute("""
    CREATE TABLE IF NOT EXISTS `Users`(
    id integer PRIMARY KEY UNIQUE,
    username text NOT NULL,
    password text NOT NULL,
    email text NOT NULL
    );
    """)

    del con


def create_table_site_logins():
    con = MySQLConnector()

    con.cursor.execute("""
        CREATE TABLE IF NOT EXISTS `SiteLogins`(
        id integer UNIQUE,
        user integer NOT NULL,
        website text NOT NULL,
        username text NOT NULL,
        password text NOT NULL,
        type text NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY (user) REFERENCES Users(id)
        );
        """)

    del con


if __name__ == '__main__':
    # create_table_user()
    # create_table_site_logins()

    con = MySQLConnector()

    # con.exec("DROP TABLE users")

    del con
