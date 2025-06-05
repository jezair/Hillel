class Add():
    def __init__(self, argument):
        self.argument = argument

    def __add__(self, other):
        return other + self.argument
z = Add(12)
x = Add(2)
t = z + x
print(t)