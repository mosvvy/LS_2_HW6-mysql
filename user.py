from sqlite3 import IntegrityError

from mysql_connector import MySQLConnector


class User:
    def __init__(self, username, password, email=None):
        """Ініціалізує нового користувача з переданими username, password та email."""
        self._id = None
        self._username = username
        self._password = password
        self._email = email

    def register(self):
        """Зберігає дані про користувача у базу даних."""

        # with SQLiteConnector() as con:
        #     con.cursor.execute("")
        #     con.commit()
        con = MySQLConnector()
        try:
            con.cursor.execute(f'SELECT COUNT(*) FROM users WHERE username = "{self._username}"')
            cnt = con.cursor.fetchall()[0][0]
            if cnt:
                raise IntegrityError

            con.cursor.execute(f'SELECT COUNT(*) FROM users WHERE email = "{self._email}"')
            cnt = con.cursor.fetchall()[0][0]
            if cnt:
                raise ValueError

            con.cursor.execute("SELECT COUNT(*) FROM users")
            cnt = con.cursor.fetchall()[0][0]

            con.cursor.execute(f"INSERT INTO users (id, username, password, email) VALUES ({cnt}, '{self._username}', '{self._password}', '{self._email}')")
            con.commit()
        except IntegrityError:
            print(f'Користувач з іменем "{self._username}" вже існує!')
        except ValueError:
            print(f'Користувач з поштою "{self._email}" вже існує!')
        del con

    def login(self, username, password):
        """Перевіряє, чи існує користувач з вказаним username та password у базі даних.
        Повертає True, якщо такий користувач існує, і False в іншому випадку."""

        con = MySQLConnector()
        con.cursor.execute(f"SELECT id FROM users WHERE username='{username}' AND password='{password}'")
        r = con.cursor.fetchall()
        # print(r[0][0])
        del con
        self._id = r[0][0]
        return bool(r[0][0])

    @staticmethod
    def show_all():
        con = MySQLConnector()
        con.cursor.execute(f"SELECT username, password, email FROM users")
        r = con.cursor.fetchall()
        del con
        return r

    def get_id(self):
        return self._id

    def get_username(self):
        return self._username


if __name__ == '__main__':
    user1 = User('uname1', 'qwerty', 'qwerty@ex.com')
    # user1.register()
    print(user1.login('uname1', 'qwerty'))
    print(user1.login('uname1', 'qwertty'))
    print(user1.login('uname2', 'qwertty'))