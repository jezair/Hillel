"""
REPOSITORY: john = Repository(User()).save()
ACTIVE RECORD: User().save()

class:
- structs
- behavioral
"""

import csv
from pathlib import Path


class Student:
    def __init__(self, id, name, marks, info):
        self.id = id
        self.name = name
        self.marks = marks
        self.info = info

    def __str__(self):
        return f"Student {self.name}"

    def as_dict(self):
        return {"name": self.name, "marks": self.marks, "info": self.info}

    @property
    def representation(self):
        return (
            "=========================\n"
            f"Student {self.name}\n"
            f"Marks: {self.marks}\n"
            f"Info: {self.info}\n"
            "=========================\n"
        )


STORAGE_FILE_NAME = Path(__file__).parent.parent / "storage/students.csv"


# ─────────────────────────────────────────────────────────
# INFRASTRUCTURE
# ─────────────────────────────────────────────────────────


class Repository:
    """
    RAM: John, Marry, Mark
    SSD: John, Marry
    """

    def __init__(self):
        try:
            self.file = open(STORAGE_FILE_NAME, "r")
            self.students = self.get_storage()
        except FileNotFoundError:
            print("Can not open storage file.")
        finally:
            self.file.close()

        self.students: dict[int, Student] = {
            student.id: student for student in self.get_storage()
        }

    def get_storage(self):
        self.file.seek(0)
        reader = csv.DictReader(
            self.file, fieldnames=["id", "name", "marks", "info"], delimiter=";"
        )

        results: list[Student] = []
        for item in reader:
            student = Student(**item)
            results.append(student)

        return results

    def __del__(self):
        # ...
        self.file.close()


repo = Repository()


def inject_repository(func):
    def inner(*args, **kwargs):
        return func(*args, repo=repo, **kwargs)

    return inner


# ─────────────────────────────────────────────────────────
# DOMAIN (student, users, notification)
# ─────────────────────────────────────────────────────────
class StudentService:
    @inject_repository
    def add_student(self, repo: Repository, student: Student) -> Student | None:
        next_id = max(repo.students.keys()) + 1
        repo.students[next_id] = student
        return student

    @inject_repository
    def show_students(self, repo: Repository):
        print("=========================\n")
        for student in repo.students.values():
            print(student.representation)
        print("=========================\n")

    def show_student(self, student: Student) -> None:
        print(student.representation)

    def update_student(self, id_: int, raw_input: str) -> Student | None:
        parsing_result = raw_input.split(";")

        if len(parsing_result) != 2:
            return None

        new_name, new_info = parsing_result

        try:
            student = Student(name=new_info, info=new_info)
        except ValueError:
            raise Exception(f"Can not update student with id={id_}")
        else:
            return student


# ─────────────────────────────────────────────────────────
# OPERATIONAL (APPLICATION) LAYER
# ─────────────────────────────────────────────────────────
def ask_student_payload() -> dict:
    ask_prompt = (
        "Enter student's payload data using text template: "
        "John Doe;1,2,3,4,5\n"
        "where 'John Doe' is a full name and [1,2,3,4,5] are marks.\n"
        "The data must be separated by ';'"
    )

    def parse(data) -> dict:
        name, raw_marks = data.split(";")

        return {
            "name": name,
            "marks": [int(item) for item in raw_marks.replace(" ", "").split(",")],
        }

    user_data: str = input(ask_prompt)
    return parse(user_data)


def student_management_command_handle(command: str):
    students_service = StudentService()
    if command == "show":
        with Repository("storage.json") as repo:
            repo.get_students()
            students_service.show_students(repo)
    elif command == "add":
        data = ask_student_payload()
        repo = Repository()
        repo.add_student(data)
        repo.students
        if data:
            student: dict | None = add_student(data)
            if student is None:
                print("Error adding student")
            else:
                print(f"Student: {student['name']} is added")
        else:
            print("The student's data is NOT correct. Please try again")
    elif command == "search":
        student_id: str = input("\nEnter student's ID: ")
        if not student_id:
            print("Student's ID is required to search")
            return

        students = get_storage()

        student: dict | None = storage.get(int(student_id))
        if student is None:
            print("Error adding student")
        else:
            show_student(student_id, students)
            print(f"Student {student_id} not found")
    elif command == "delete":
        student_id: str = input("\nEnter student's ID: ")
        if not student_id:
            print("Student's id is required to delete")
            return

        id_ = int(student_id)
        if storage.get(id_):
            del storage[id_]
    elif command == "update":
        student_id: str = input("\nEnter student's ID: ")
        if not student_id:
            print("Student ID must be specified for update")
            return

        id_ = int(student_id)
        student: dict | None = storage.get(id_)
        if student is None:
            print(f"Student {student_id} not found")
            return

        show_student(student)
        print(
            f"\n\nTo update user's data, specify `name` and `info`, with `;` separator.\n"
        )

        user_input: str = input("Enter: ")
        updated_student: dict | None = update_student(id_=id_, raw_input=user_input)

        if updated_student is None:
            print("Erorr on updating student")
        else:
            print(f"Student {updated_student['name']} is updated")
    else:
        raise InvalidUserInput


# ─────────────────────────────────────────────────────────
# PRESENTATION LAYER
# ─────────────────────────────────────────────────────────


class InvalidUserInput(Exception):
    pass


def handle_user_input():
    OPERATIONAL_COMMANDS = ("quit", "help")
    STUDENT_MANAGEMENT_COMMANDS = ("show", "add", "search", "delete", "update")
    AVAILABLE_COMMANDS = (*OPERATIONAL_COMMANDS, *STUDENT_MANAGEMENT_COMMANDS)

    HELP_MESSAGE = (
        "Hello in the Journal! User the menu to interact with the application.\n"
        f"Available commands: {AVAILABLE_COMMANDS}"
    )

    print(HELP_MESSAGE)

    while True:
        command = input("\n Select command: ")

        if command == "quit":
            print("\nThanks for using the Journal application")
            break
        elif command == "help":
            print(HELP_MESSAGE)
        else:
            student_management_command_handle(command)


# ─────────────────────────────────────────────────────────
# ENTRYPOINT
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        handle_user_input()
    except InvalidUserInput as error:
        print(error)
    except Exception:
        pass
