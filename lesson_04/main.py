import csv
from pathlib import Path
# ─────────────────────────────────────────────────────────
# STORAGE SIMULATION
# ─────────────────────────────────────────────────────────
storage: dict[int, dict] = {
    1: {
        "name": "Alice Johnson",
        "marks": [7, 8, 9, 10, 6, 7, 8],
        "info": "Alice Johnson is 18 y.o. Interests: math",
    },
    2: {
        "name": "Michael Smith",
        "marks": [6, 5, 7, 8, 7, 9, 10],
        "info": "Michael Smith is 19 y.o. Interests: science",
    },
    3: {
        "name": "Emily Davis",
        "marks": [9, 8, 8, 7, 6, 7, 7],
        "info": "Emily Davis is 17 y.o. Interests: literature",
    },
    4: {
        "name": "James Wilson",
        "marks": [5, 6, 7, 8, 9, 10, 11],
        "info": "James Wilson is 20 y.o. Interests: sports",
    },
    5: {
        "name": "Olivia Martinez",
        "marks": [10, 9, 8, 7, 6, 5, 4],
        "info": "Olivia Martinez is 18 y.o. Interests: art",
    },
    6: {
        "name": "Emily Davis",
        "marks": [4, 5, 6, 7, 8, 9, 10],
        "info": "Daniel Brown is 19 y.o. Interests: music",
    },
    7: {
        "name": "Sophia Taylor",
        "marks": [11, 10, 9, 8, 7, 6, 5],
        "info": "Sophia Taylor is 20 y.o. Interests: physics",
    },
    8: {
        "name": "William Anderson",
        "marks": [7, 7, 7, 7, 7, 7, 7],
        "info": "William Anderson is 18 y.o. Interests: chemistry",
    },
    9: {
        "name": "Isabella Thomas",
        "marks": [8, 8, 8, 8, 8, 8, 8],
        "info": "Isabella Thomas is 19 y.o. Interests: biology",
    },
    10: {
        "name": "Benjamin Jackson",
        "marks": [9, 9, 9, 9, 9, 9, 9],
        "info": "Benjamin Jackson is 20 y.o. Interests: history",
    },
}


STORAGE_FILE_NAME = Path(__file__).parent.parent / "storage/students.csv"


# ─────────────────────────────────────────────────────────
# INFRASTRUCTURE
# ─────────────────────────────────────────────────────────

class Repository:
    def __init__(self):
        self.file_path = STORAGE_FILE_NAME
        self.students: dict[int, dict] = {}
        self.load_storage()

    def load_storage(self):
        self.students = {}
        if not self.file_path.exists():
            return
        with open(self.file_path, "r", newline='') as f:
            reader = csv.DictReader(f, delimiter=";", fieldnames=["id", "name", "marks", "info"])
            for row in reader:
                try:
                    id_ = int(row["id"])
                    marks = [int(m.strip()) for m in row["marks"].split(",") if m.strip().isdigit()]
                    self.students[id_] = {
                        "name": row["name"],
                        "marks": marks,
                        "info": row["info"]
                    }
                except (ValueError, TypeError):
                    continue

    def save_storage(self):
        with open(self.file_path, "w", newline='') as f:
            writer = csv.DictWriter(f, delimiter=";", fieldnames=["id", "name", "marks", "info"])
            for id_, student in self.students.items():
                writer.writerow({
                    "id": id_,
                    "name": student["name"],
                    "marks": ",".join(map(str, student["marks"])),
                    "info": student["info"]
                })

    def add_student(self, student: dict):
        new_id = max(self.students.keys(), default=0) + 1
        self.students[new_id] = student
        self.save_storage()

    def get_student(self, id_: int) -> dict | None:
        return self.students.get(id_)

    def update_student(self, id_: int, data: dict):
        student = self.students.get(id_)
        if not student:
            return
        student.update(data)
        self.save_storage()

    def delete_student(self, id_: int):
        if id_ in self.students:
            del self.students[id_]
            self.save_storage()

    def add_mark(self, id_: int, mark: int):
        student = self.students.get(id_)
        if student:
            student["marks"].append(mark)
            self.save_storage()

    def get_all(self) -> dict[int, dict]:
        return self.students


repo = Repository()

def inject_repository(func):
    def inner(*args, **kwargs):
        return func(*args, repo=repo, **kwargs)

    return inner



# ─────────────────────────────────────────────────────────
# DOMAIN (student, users, notification)
# ─────────────────────────────────────────────────────────
class StudentService:
    def __init__(self, repository: Repository):
        self.repository = repository

    def add_student(self, student: dict):
        self.repository.add_student(student)

    def show_students(self):
        students = self.repository.get_all()
        print("=========================\n")
        for id_, student in students.items():
            print(f"{id_}. Student {student['name']}")
        print("=========================\n")

    def show_student(self, id_: int):
        student = self.repository.get_student(id_)
        if student:
            print(
                "=========================\n"
                f"Student {student['name']}\n"
                f"Marks: {student['marks']}\n"
                f"Info: {student['info']}\n"
                "=========================\n"
            )
        else:
            print(f"Student with id {id_} not found.")

    def update_student(self, id_: int, raw_input: str):
        parts = raw_input.split(";")
        if len(parts) != 2:
            print("Invalid format. Use: New Name;New Info")
            return
        name, info = parts
        self.repository.update_student(id_, {"name": name, "info": info})
        print(f"Student {id_} updated")

    def delete_student(self, id_: int):
        self.repository.delete_student(id_)
        print(f"Student {id_} deleted")

    def add_mark(self, id_: int, mark: int):
        self.repository.add_mark(id_, mark)
        print(f"Mark {mark} added to student {id_}")



# ─────────────────────────────────────────────────────────
# OPERATIONAL (APPLICATION) LAYER
# ─────────────────────────────────────────────────────────
def ask_student_payload() -> dict:
    ask_prompt = (
        "Enter student's data in the format:\n"
        "Full Name;1,2,3,4,5;Some info about the student\n"
        "Example: John Doe;1,2,3,4,5;Interested in physics\n> "
    )

    def parse(data: str) -> dict:
        try:
            name, raw_marks, info = data.strip().split(";")
            marks = [int(item) for item in raw_marks.replace(" ", "").split(",")]
            return {
                "name": name.strip(),
                "marks": marks,
                "info": info.strip()
            }
        except ValueError:
            print("Invalid input format. Please use: Name;1,2,3;Info")
            return {}

    user_data = input(ask_prompt)
    return parse(user_data)

def student_management_command_handle(command: str, service: StudentService):
    if command == "show":
        service.show_students()
    elif command == "add":
        data = ask_student_payload()
        service.add_student(data)
    elif command == "search":
        id_ = int(input("Enter student ID: "))
        service.show_student(id_)
    elif command == "update":
        id_ = int(input("Enter student ID: "))
        service.show_student(id_)
        new_data = input("Enter new name and info separated by ';': ")
        service.update_student(id_, new_data)
    elif command == "delete":
        id_ = int(input("Enter student ID to delete: "))
        service.delete_student(id_)
    elif command == "addmark":
        id_ = int(input("Enter student ID to add mark: "))
        mark = int(input("Enter mark: "))
        service.add_mark(id_, mark)



# ─────────────────────────────────────────────────────────
# PRESENTATION LAYER
# ─────────────────────────────────────────────────────────
def handle_user_input():
    COMMANDS = ("show", "add", "search", "update", "delete", "addmark", "quit", "help")
    HELP = f"Available commands: {', '.join(COMMANDS)}"

    print(HELP)
    repo = Repository()
    service = StudentService(repo)

    while True:
        command = input("Command: ").strip().lower()
        if command == "quit":
            print("Goodbye!")
            break
        elif command == "help":
            print(HELP)
        elif command in COMMANDS:
            student_management_command_handle(command, service)
        else:
            print("Unknown command. Type 'help' to see available options.")



# ─────────────────────────────────────────────────────────
# ENTRYPOINT
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    handle_user_input()
