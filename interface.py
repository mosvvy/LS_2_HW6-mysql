import re

from site_login import SiteLogin
from user import User


class Menu:
    _user: User | None

    def __init__(self):
        self.__menu_items = {}
        self._user = None

    def __get_choice(self):
        print()
        print(f'Ви увійшли як {self._user.get_username()}.' if self._user else 'Привіт, Гість!')
        for cmd, (_, description) in self.__menu_items.items():
            print(f'{cmd} - {description}')

        return input('Введіть номер дії: ')

    def set_user(self, user: User):
        self._user = user

    def get_user(self):
        return self._user

    def add_handler(self, cmd, description):
        def wrapper(func):
            self.__menu_items[cmd] = (func, description)
            return func

        return wrapper

    def run(self):
        is_continue = True
        while is_continue:
            choice = self.__get_choice()
            func, _ = self.__menu_items.get(choice, (default, ''))
            is_continue = func()


menu = Menu()


def add_email():
    pattern = r'[a-zA-Z0-9]*@[a-zA-Z0-9]{2,10}.[a-zA-Z0-9]{2,4}'
    while True:
        value = input('Введіть адресу ел.пошти: ')
        if value == '':
            break
        if re.match(pattern, value):
            return value
        print('Пошта невалідна. Будь-ласка спробуйте ще раз.\n\t'
              'Електронна адреса має складатися з латинських літер та цифр, мфти комерційну ет та крапку\n\t'
              'Пустий рядок скасує реєстрацію.')


@menu.add_handler('1', 'Зареєструватися')
def menu_register():
    """Якщо користувач обирає зареєструватися, програма має
    запитати username, password та email,
    створити нового користувача і зберегти його в базу даних."""
    username = input("Введіть ім'я користувача: ")
    password = input('Введіть пароль: ')
    email = add_email()
    if not email:
        return True
    new_user = User(username, password, email)
    new_user.register()
    return True


@menu.add_handler('2', 'Увійти')
def menu_login():
    """Якщо користувач обирає увійти, програма має запитати username та password,
    потім перевірити, чи існує такий користувач у базі даних.
    Якщо так, вивести повідомлення "Успішний вхід!", інакше - "Неправильні дані!" """
    username = input("Введіть ім'я користувача: ")
    password = input('Введіть пароль: ')
    new_user = User(username, password)
    login_result = new_user.login(username, password)
    if login_result:
        menu.set_user(new_user)
        print('Успішний вхід!')
    else:
        print('Неправильні дані!')
    return True


@menu.add_handler('3', 'Додати параметри входу')
def menu_add_login():
    if menu.get_user() is None:
        print('Увійдіть в систему будь-ласка.')
        return True

    website = input('Введіть адресу сайту: ')
    username = input("Введіть ім'я користувача: ")
    password = None

    print('Вхід за допомогою:')
    for cmd, desc in SiteLogin.auth_types.items():
        print(f'{cmd} - {desc}')
    auth_type_key = input('Введіть ресурс інтеграції або залиште пустим: ')
    auth_type = SiteLogin.auth_types.get(auth_type_key)

    if auth_type == 'Other':
        auth_type = input('Вкажіть ресурс, за яким відбуваєтсья вхід: ')

    if auth_type is None:
        password = input('Введіть пароль: ')

    auth = SiteLogin(menu.get_user())
    auth.save(website, username, password, auth_type)

    return True


@menu.add_handler('4', 'Переглянути збережені параметри входу')
def menu_show_logins():
    if menu.get_user() is None:
        print('Увійдіть в систему будь-ласка.')
        return True

    auth = SiteLogin(menu.get_user())

    pattern = '{:>20} | {:<20} | {:<20} | {}'
    print(pattern.format('website', 'username', 'password', 'type'))
    print(pattern.format('-' * 20, '-' * 20, '-' * 20, '-' * 20))
    for user in auth.show_all():
        print(pattern.format(user[0], user[1], user[2], user[3]))

    return True


@menu.add_handler('5', 'Вийти')
def menu_exit():
    """Якщо користувач обирає вийти, програма має завершити роботу."""
    return False


@menu.add_handler('0', 'Показати всіх користувачів')
def menu_show_all():
    """Допоміжна функція, що виводить інформацію про найвних користувачів."""
    pattern = '{:>20} | {:<20} | {}'
    print(pattern.format('username', 'password', 'email'))
    print(pattern.format('-' * 20, '-' * 20, '-' * 20))
    for user in User.show_all():
        print(pattern.format(user[0], user[1], user[2]))
    return True


def default():
    print('Невідома дія. Будь-ласка, спробуйте ще раз.')
    return True


if __name__ == '__main__':
    menu.run()
