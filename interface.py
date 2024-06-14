import re

from user import User


class Menu:
    def __init__(self):
        self.__menu_items = {}

    def __get_choice(self):
        print()
        for cmd, (_, description) in self.__menu_items.items():
            print(f'{cmd} - {description}')

        return input('Введіть номер дії: ')

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
        print('Пошта невалідна. Будь-ласка спробуйте ще раз.\n\tЕлектронна адреса має складатися з латинських літер та цифр, мфти комерційну ет та крапку\n\tПустий рядок скасує реєстрацію.')


# TODO checks and catches
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
        print('Успішний вхід!')
    else:
        print('Неправильні дані!')
    return True


@menu.add_handler('3', 'Вийти')
def menu_exit():
    """Якщо користувач обирає вийти, програма має завершити роботу."""
    return False


@menu.add_handler('0', 'Показати всіх користувачів')
def menu_show_all():
    """Допоміжна функція, що виводить інформацію про найвних користувачів."""
    pattern = '{:>20} | {:<20} | {}'
    print(pattern.format('username', 'password', 'email'))
    print(pattern.format('-'*20, '-'*20, '-'*20))
    for user in User.show_all():
        print(pattern.format(user[0], user[1], user[2]))
    return True


def default():
    print('Невідома дія. Будь-ласка, спробуйте ще раз.')
    return True


if __name__ == '__main__':
    menu.run()
