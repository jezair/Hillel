import csv
from pathlib import Path


class Student:
    def __init__(self, id, name, marks, info):
        self.id = int(id)
        self.name = name
        self.marks = [int(m) for m in marks.split(",")] if isinstance(marks, str) else marks
        self.info = info

    def __str__(self):
        return f"Student {self.name}"

    def as_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "marks": ",".join(map(str, self.marks)),
            "info": self.info,
        }

    @property
    def representation(self):
        return (
            "=========================\n"
            f"Student {self.name}\n"
            f"Marks: {self.marks}\n"
            f"Info: {self.info}\n"
            "=========================\n"
        )


class Admin:
    def __init__(self, id, login, password):
        self.id = id
        self.login = login
        self.password = password

    def __str__(self):
        return f"Admin {self.login}"


authorized_admin = None

ADMIN_FILE_NAME = Path(__file__).parent.parent / "storage/admins.csv"
STORAGE_FILE_NAME = Path(__file__).parent.parent / "storage/students.csv"


def load_admins():
    with open(ADMIN_FILE_NAME, newline="") as admins_csv:
        reader = csv.DictReader(admins_csv, delimiter=";")
        return [Admin(row["id"], row["login"], row["password"]) for row in reader]


def auth(func):
    global authorized_admin

    def wrapper(*args, **kwargs):
        admins = load_admins()
        while True:
            log = input("Enter login:\n")
            pas = input("Enter password:\n")
            matched = next((a for a in admins if a.login == log and a.password == pas), None)
            if matched:
                authorized_admin = matched
                print("Enjoy")
                break
            else:
                print("Login or password incorrect")
        return func(*args, **kwargs)

    return wrapper


class Repository:
    def __init__(self):
        self.students: dict[int, Student] = {
            student.id: student for student in self.get_storage()
        }

    def get_storage(self):
        with open(STORAGE_FILE_NAME, newline="") as f:
            reader = csv.DictReader(f, fieldnames=["id", "name", "marks", "info"], delimiter=";")
            return [Student(**row) for row in reader]

    def save_all(self):
        with open(STORAGE_FILE_NAME, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "name", "marks", "info"], delimiter=";")
            for student in self.students.values():
                writer.writerow(student.as_dict())


repo = Repository()


def inject_repository(func):
    def inner(*args, **kwargs):
        return func(*args, repo=repo, **kwargs)
    return inner


class StudentService:
    @inject_repository
    def add_student(self, repo: Repository, student: Student) -> Student:
        next_id = max(repo.students.keys(), default=0) + 1
        student.id = next_id
        repo.students[next_id] = student
        repo.save_all()
        return student

    @inject_repository
    def show_students(self, repo: Repository):
        for student in repo.students.values():
            print(student.representation)

    @inject_repository
    def get(self, id_: int, repo: Repository) -> Student | None:
        return repo.students.get(id_)

    @inject_repository
    def update_student(self, id_: int, raw_input: str, repo: Repository) -> Student | None:
        if id_ not in repo.students:
            return None

        parsing_result = raw_input.split(";")
        if len(parsing_result) != 2:
            return None

        new_name, new_info = parsing_result
        student = repo.students[id_]
        student.name = new_name.strip()
        student.info = new_info.strip()
        repo.save_all()
        return student

    @inject_repository
    def delete(self, id_: int, repo: Repository):
        if id_ in repo.students:
            del repo.students[id_]
            repo.save_all()


def ask_student_payload() -> dict:
    ask_prompt = (
        "Enter student's data (Example: John Doe;1,2,3,4,5):\n"
        "where name is full name and marks is comma-separated numbers.\n"
    )

    user_data = input(ask_prompt)
    name, raw_marks = user_data.split(";")
    return {
        "name": name.strip(),
        "marks": [int(m) for m in raw_marks.replace(" ", "").split(",")],
        "info": "No info"  # or ask for it separately
    }


def student_management_command_handle(command: str):
    students_service = StudentService()

    if command == "show":
        students_service.show_students()

    elif command == "add":
        data = ask_student_payload()
        student = Student(id=0, name=data["name"], marks=data["marks"], info=data["info"])
        students_service.add_student(student)
        print(f"Student '{student.name}' added")

    elif command == "delete":
        id_ = int(input("Enter student's ID: "))
        students_service.delete(id_)
        print(f"Student {id_} deleted")

    elif command == "update":
        id_ = int(input("Enter student's ID: "))
        student = students_service.get(id_)
        if not student:
            print("Student not found")
            return

        print("Existing student:")
        print(student.representation)

        print("Enter new name and info (format: New Name;New Info)")
        raw_input = input("Enter: ")
        updated = students_service.update_student(id_, raw_input)
        if updated:
            print("Student updated successfully")
        else:
            print("Error updating student")


@auth
def handle_user_input():
    COMMANDS = ("quit", "help", "show", "add", "delete", "update")
    print(f"Welcome to Journal. Available commands: {COMMANDS}")

    while True:
        command = input("\nEnter command: ").strip()
        if command == "quit":
            print("Bye!")
            break
        elif command == "help":
            print(f"Available commands: {COMMANDS}")
        elif command in COMMANDS:
            student_management_command_handle(command)
        else:
            print("Unknown command")


if __name__ == "__main__":
    handle_user_input()
