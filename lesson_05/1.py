import inspect


class User:
    def __init__(self, login: str, password: str, balance: int):
        self.login: str = login
        self.password: str = password
        self.balance: int = balance

class Database:
    users = {
        1: User(
            login="john",
            password="john",
            balance=0
        ),
        2: User(
            login="marry",
            password="marry",
            balance = 0,
        ),
    }


class PaymentSystem:
    def __init__(self, user: User):
        self.connected_to_the_atm = False
        self.user: User = user


    def deposit(self, amount: int):
        self.user.balance += amount
        print(f"Deposit {amount} to {self.user.balance}")
        print(f"TOTAL: {self.user.balance}")

    def withdraw(self, amount: int):
        self._validate_money()
        self._connect_to_the_atm()
        self._count_the_cash(amount)
        self._get_money(amount)

    def _validate_money(self):
        if self.user.balance < 0:
            print("Cannot deposit money")

    def _connect_to_the_atm(self):
        self.connected_to_the_atm = True
        print("Connected to ATM")

    def _count_the_cash(self, amount: int):
        if self.connected_to_the_atm is True:
            print(f"Counting {amount} in the ATM")
        else:
            print("Something went wrong")

    def _get_money(self, amount: int):
        if self.connected_to_the_atm is True:
            self.user.balance -= amount
            print(f"Returning money from ATM")
        else:
            print("Something went wrong")


    def balance(self):
        print(self.user_repr)


    @property
    def user_repr(self):
        self.msg = ...
        return f"User {self.user.login}, balance: {self.user.balance}"

    @user_repr.setter
    def user_repr(self, value):
        if "admin:" in value:
            return value.replace("admin:", "")
        else:
            raise ValueError("Can not set value")


    # def __getattr__(self, item: str):
    #     print(f"Attribute: {item} not found")

    # NOTE: bad idea...
    # def __getattribute__(self, name: str):
    #     breakpoint()  # TODO: remove
    #     if name.startswith("_"):
    #         stack = inspect.stack()
    #         print("Stack at attribute")
    #
    #         for i, frame in enumerate(stack[0:4]):
    #             print(f"Frame {i}: {frame.function}, {frame.filename}")
    #
    #         if not any(
    #             (frame.frame.f_locals.get("self", None) is self for frame in stack[1:3])
    #         ):
    #             raise AttributeError(f"Access to attribute {name} restricted")
    #
    #     return super().__getattribute__(name)


def main():
    user = Database.users[1]
    payment_system = PaymentSystem(user=user)

    payment_system.deposit(100)
    payment_system.withdraw(10)
    payment_system.balance()

    payment_system.user_repr = "admin:hacked"
    payment_system.balance()

    # payment_system._get_money(20)
    # payment_system.balance()

if __name__ == "__main__":
    main()
