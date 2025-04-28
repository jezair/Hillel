def foo(arg1, *args, **kwargs):
    pass


foo(12, "test", 13, 14, name="hello")


# contact_info = "john,doe,nyst 12 av,+3807711000,male"
# name, *_, phone, sex = contact_info.split(",")

# name, phone, *_ = ["john", "doe", "nyst 12 av", "+3807711000", "male"]
# print(name, phone)
# print(name)
# print(phone)
# print(sex)
