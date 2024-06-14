import sqlite3


class SQLiteConnector:
    __cursor:sqlite3.Cursor

    def __init__(self, path:str='auth_db.db'):
        self.__path = path
        self.__connection = sqlite3.connect(self.__path)
        self.__cursor = self.__connection.cursor()

    @property
    def cursor(self):
        return self.__cursor

    def exec(self, query:str):
        return  self.__cursor.execute(query)

    def commit(self):
        self.__connection.commit()

    def __del__(self):
        self.__cursor.close()
        self.__connection.close()


def create_table_user():
    con = SQLiteConnector('auth_db.db')

    con.cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
    id integer PRIMARY KEY AUTOINCREMENT,
    username text unique,
    password text,
    email text unique
    );
    """)

    del con


if __name__ == '__main__':
    # create_table_user()

    con = SQLiteConnector('auth_db.db')

    # con.exec("DROP TABLE users")

    del con
