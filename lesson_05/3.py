def auth(func):
    def wrapper(*args, **kwargs):
        user = input("Введи логин: ")
        password = input("Введи пароль: ")
        if user == "admin" and password == "1234":
            print("Доступ разрешен.")
            return func(*args, **kwargs)
        else:
            print("Доступ запрещен.")
    return wrapper

@auth
def secret_data():
    print("Вот секретные данные!")

secret_data()
