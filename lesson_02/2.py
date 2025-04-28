"""
User  ->  login
User  ->  password
"""

user = {
    "name": "John",
    "login": "john",
    "passwrod": "124",
}


authenticated = False


login = input("enter login: ")
password = input("enter password: ")


if login == user["login"] and password == user["passwrod"]:
    authenticated = True

if not authenticated:
    login = input("enter login: ")
    password = input("enter password: ")

    if login == user["login"] and password == user["passwrod"]:
        authenticated = True

if not authenticated:
    login = input("enter login: ")
    password = input("enter password: ")

    if login == user["login"] and password == user["passwrod"]:
        authenticated = True
if not authenticated:
    login = input("enter login: ")
    password = input("enter password: ")

    if login == user["login"] and password == user["passwrod"]:
        authenticated = True

if not authenticated:
    if login == user["login"] and password == user["passwrod"]:
        authenticated = True
