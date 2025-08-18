import enum

class Role(enum.StrEnum):
    STUDENT = enum.auto()
    TEACHER = enum.auto()

class User:
    def __init__(self, name: str, email: str, role: Role) -> None:
        self.name = name
        self.email = email
        self.role = role

    def send_notification(self, notification):
        print(notification)

class Notification:
    def __init__(self, subject: str, message: str, attachment: str = "") -> None:
        self.subject = subject
        self.message = message
        self.attachment = attachment

    def __str__(self):
        base = f"Message from {self.subject}\nMessage: {self.message}\nAttachment: {self.attachment}"
        return base

class StudentNotification(Notification):
    def __str__(self):
        return f"Sent via Student Portal\n" + super().__str__()

class TeacherNotification(Notification):
    def __str__(self):
        return f"Teacher's Desk Notification\n" + super().__str__()

def main():
    student  = User("Viktor", "stud@email.com", Role.STUDENT)
    teacher  = User("Alice", "teacher@email.com", Role.TEACHER)

    note_for_student  = StudentNotification("Teacher", "Hello Student, where is you homework?")
    note_for_teacher  = TeacherNotification("Student", "Hello Teacher, I wanna more marks!")

    student.send_notification(note_for_student)
    print("-" * 50)
    teacher.send_notification(note_for_teacher)

if __name__ == "__main__":
    main()