"""
реалізуємо додатково таблицю, в якій ви створити можливість додавати інформацію про реєстрацію на різних сайтах та зберігати її.
Для цього реалізуйте клас, всередині якого будуть відповідні методи.
Ми будемо зберігати інформацію про назву сайту, логін, пароль, вид входу (google, Apple, Facebook або інша)
та приналежність їх до певного користувача,
що робиться за допомогою зовнішнього ключа до колонки ідентифікатора в попередній таблиці.

реалізуйте функціонал, де кожен користувач, який зареєстрований може створювати та виводити на екран інформацію про сайте,
на яких він зареєстрований. Це буде просто з вікна терміналу за допомогою методів текстового введення.
Єдине, що слід передбачити це те, якщо людина до єднуються до сайту ще раз спеціальний вид входу,
то про логін та пароль питати не треба.
"""
from mysql.connector import IntegrityError
from mysql_connector import MySQLConnector
from user import User


class SiteLogin:
    auth_types = {
        1: 'Google',
        2: 'Apple',
        3: 'Facebook',
        0: 'Other', # todo specify it
    }

    def __init__(self, user: User):
        self._user = user

    def save(self, website, username, password, auth_type):
        con = MySQLConnector()
        try:
            # todo add validation
            # todo add check on duplicating
            # con.cursor.execute(f'SELECT COUNT(*) FROM users WHERE username = "{self._username}"')
            # cnt = con.cursor.fetchall()[0][0]
            # if cnt:
            #     raise IntegrityError
            #
            # con.cursor.execute(f'SELECT COUNT(*) FROM users WHERE email = "{self._email}"')
            # cnt = con.cursor.fetchall()[0][0]
            # if cnt:
            #     raise ValueError

            user = self._user._id  # todo clear using protected field

            con.cursor.execute("SELECT COUNT(*) FROM sitelogins")
            cnt = con.cursor.fetchall()[0][0]

            con.cursor.execute(f"INSERT INTO sitelogins (id, user, website, username, password, type) "
                               f"VALUES ({cnt}, '{user}', '{website}', '{username}', '{password}', '{auth_type}')")
            con.commit()
        except IntegrityError:
            print(f'Користувач з іменем "{user}" вже існує!')
        except ValueError:
            print(f'Користувач з поштою "{user}" вже існує!')
        del con

    def show_all(self):
        con = MySQLConnector()
        con.cursor.execute(f"SELECT website, username, password, type FROM sitelogins WHERE user={self._user._id}")
        r = con.cursor.fetchall()
        del con
        return r