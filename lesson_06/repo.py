

class Repository:
    def __init__(self, filename: str):
        self.filename = filename
        self.file:IOTextWSr


    def __enter__(self):
        file = open(self.filename, "r")
        setattr(self, "_file", file)
        self.data = file.read()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._file is None:
            return
        else:
            self._file.write(self.data)
            self._file.close()
        # if (file := getattr(self, "_file", None)) is not None:
        #     print("Closing the file ")
        #     file.close()
        #     return
        # else:
        #     return

    def add_student(self):



with Repository("storage.json") as repo:
    students = repo.get_students()
    repo.add_student()
    repo.get_student()

