import mysql.connector


class MySQLConnector:
    # __cursor:sqlite3.Cursor

    def __init__(self, host: str = 'localhost', user: str = 'root', password: str = 'qwerty', db_name: str = 'hw_6_db'):
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


if __name__ == '__main__':
    # create_table_user()

    con = MySQLConnector()

    # con.exec("DROP TABLE users")

    del con
