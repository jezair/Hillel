# Agenda

- Multiprocessing
- WEB Introduction

# Multiprocessing

- run only in `__main__`

## basic example

```python
import time
from multiprocessing import Process


def foo():
    print("another process started")
    time.sleep(10)


if __name__ == "__main__":
    process = Process(target=foo)
    process.run()
```

## communication via `multiprocessing.Queue`

```python
from multiprocessing import Process, Queue


def worker(q: Queue):
    q.put("Hello from worker")


if __name__ == "__main__":
    q  = Queue()
    process = Process(target=worker, args=(q,))
    process.run()
    print(q.get())  # output

```

## Manager in multiprocessing for other data structures

```python
from multiprocessing import Manager, Process


def add_student(shared_students, student):
    shared_students.append(student)


if __name__ == "__main__":
    students = []
    with Manager() as manager:
        process = Process(
            target=add_student,
            args=(
                students,
                {"name": "John"},
            ),
        )
        process.run()

```

## `multiprocessing.Pool` usage

```python
import time
from multiprocessing import Pool


def square(x: int):
    time.sleep(5)
    return x * x


if __name__ == "__main__":
    with Pool() as pool:
        results = pool.map(square, [1, 2, 3, 4, 5, 6, 7, 8])
        print(results)
```

### students example

```python
from multiprocessing import Pool


def calculate_average(student):
    avg = sum(student["marks"]) / len(student["marks"])
    return avg


if __name__ == "__main__":
    students = {}

    with Pool(4) as pool:
        averages = pool.map(calculate_average, students.values())
        print(averages)
```

## Processes creation

1. `fork()`
   - new process - copy of parent process
   - fast start
   - Unix
   - problematic for CUDA
2. `spawn()`
   - new process - created from scratch
   - slow start
   - Windows, default on MacOS (python3.8+)
     - `__name__ == "__main__"`
3. `forkserver`

```python
from multiprocessing import get_start_method, set_start_method


set_start_method("fork")
print(get_start_method())
```

# WEB Introduction

## INTERNET is

- connection of all the computers
- network of local networks
- information exchange
- users tracking

phisical

- computer -> router -> router -> (switch) -> computer

## HTTP Protocol

1. version ()
2. URL (path)
3. METHOD
   1. GET
   2. POST
   3. PUT
   4. DELETE
4. Status Code
5. body?
6. headers

`HTTP GET /users`

```json
// status: 400
{
  "msg": "no password"
}
```

```json
// status: 200
{
    "msg": "no password"
    "error": true
}
```
