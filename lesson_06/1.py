def foo():
    print("started")
    item = yield 20

    print("I am here")
    if item > 30:
        yield "more than 30"
    else:
        yield "less than 30"


gen = foo()

print(next(gen))
print(gen.send(29))
