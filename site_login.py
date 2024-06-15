from mysql.connector import IntegrityError
from mysql_connector import MySQLConnector
from user import User


class SiteLogin:
    auth_types = {
        '1': 'Google',
        '2': 'Apple',
        '3': 'Facebook',
        '0': 'Other',
    }

    def __init__(self, user: User):
        self._user = user

    def save(self, website, username, password, auth_type):
        con = MySQLConnector()
        try:
            con.cursor.execute(f'SELECT COUNT(*) FROM sitelogins '
                               f'WHERE website = "{website}" AND username = "{username}" AND auth_type = "{auth_type}"')
            cnt = con.cursor.fetchall()[0][0]
            if cnt:
                raise IntegrityError

            user = self._user.get_id()

            con.cursor.execute("SELECT COUNT(*) FROM sitelogins")
            cnt = con.cursor.fetchall()[0][0]

            con.cursor.execute(f"INSERT INTO sitelogins (id, user, website, username, password, type) "
                               f"VALUES ({cnt}, '{user}', '{website}', '{username}', '{password}', '{auth_type}')")
            con.commit()
        except IntegrityError:
            print(f'Користувач з іменем "{username}" на сайті "{website}" вже існує!')
        del con

    def show_all(self):
        con = MySQLConnector()
        con.cursor.execute(f"SELECT website, username, password, type FROM sitelogins WHERE user={self._user.get_id()}")
        r = con.cursor.fetchall()
        del con
        return r
