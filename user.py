from sqlite3 import IntegrityError

from sqlite_connector import SQLiteConnector


class User:
    def __init__(self, username, password, email=None):
        """Ініціалізує нового користувача з переданими username, password та email."""
        self._username = username
        self._password = password
        self._email = email

    def register(self):
        """Зберігає дані про користувача у базу даних."""

        # with SQLiteConnector() as con:
        #     con.cursor.execute("")
        #     con.commit()
        con = SQLiteConnector()
        try:
            con.cursor.execute(f"INSERT INTO users (username, password, email) VALUES ('{self._username}', '{self._password}', '{self._email}')")
            con.commit()
        except IntegrityError:
            print(f'Користувач з іменем "{self._username}" вже існує!')
        del con

    def login(self, username, password):
        """Перевіряє, чи існує користувач з вказаним username та password у базі даних.
        Повертає True, якщо такий користувач існує, і False в іншому випадку."""

        con = SQLiteConnector()
        con.cursor.execute(f"SELECT COUNT(*) FROM users WHERE username='{username}' AND password='{password}'")
        r = con.cursor.fetchall()
        # print(r[0][0])
        del con
        return bool(r[0][0])

    @staticmethod
    def show_all():
        con = SQLiteConnector()
        con.cursor.execute(f"SELECT username, password, email FROM users")
        r = con.cursor.fetchall()
        del con
        return r


if __name__ == '__main__':
    user1 = User('uname1', 'qwerty', 'qwerty@ex.com')
    # user1.register()
    print(user1.login('uname1', 'qwerty'))
    print(user1.login('uname1', 'qwertty'))
    print(user1.login('uname2', 'qwertty'))