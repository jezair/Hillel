# Glossary

Concurrency

- Structure the program to handle multiple tasks at once

Paralellism

- about CPU cores

## CountDown Task (stop the thread)

```python
import threading
import time


class CoutdownTask:
    def __init__(self) -> None:
        self._running = True

    def run(self, n):
        while self._running and n > 0:
            print(f"T", n)
            n -= 1
            time.sleep(1)

    def terminate(self):
        self._running = False



# countdown()
c = CoutdownTask()
t = threading.Thread(target=c.run, args=(10,))
t.start()

c.terminate()
t.join()
```

## inherited from threading.Thread

```python
import threading
import time


class CoutdownTask(threading.Thread):
    def __init__(self, n) -> None:
        super().__init__()
        self.n = n

    def run(self):
        while self.n > 0:
            print(f"T", self.n)
            self.n -= 1
            time.sleep(1)


# countdown()
CoutdownTask(10).start()

```

## timer with interval

```python
import threading
import time


class Timer:
    def __init__(self, interval) -> None:
        self._interval = interval
        self._flag = 0
        self._cv = threading.Condition()

    def start(self):
        t = threading.Thread(target=self.run, daemon=True)
        t.start()

    def wait_for_tick(self):
        """Run the timer and notify waiting threads (after interval)"""

        with self._cv:
            last_flag = self._flag
            while last_flag == self._flag:
                self._cv.wait()

    def run(self):
        """Wait for the next timer triggered."""

        while True:
            time.sleep(self._interval)
            with self._cv:
                self._flag ^= 1
                self._cv.notify_all()


timer = Timer(5)
timer.start()


def foo(ticks):
    while ticks > 0:
        timer.wait_for_tick()
        print(f"T: {ticks}")
        ticks -= 1


def bar(last):
    n = 0
    while n < last:
        timer.wait_for_tick()
        print(f"Counting: {n}")
        n += 1


threading.Thread(target=foo, args=(10,)).start()
threading.Thread(target=bar, args=(5,)).start()
```

## Semaphore

```python
import threading
import time


def worker(name: str, sema: threading.Semaphore):
    # waiting
    sema.acquire()

    # process
    print(f"{name=}")


sema = threading.Semaphore(0)

for i in range(10):
    t = threading.Thread(target=worker, args=(f"john-{i}", sema))
    t.start()
```

## Producer / Consumer (publisher / subscriber), EDA

```python
"""
EDA (event driven architecture)

producer / consumer
"""

import random
import time
from queue import Queue
from threading import Thread


def producer(queue: Queue):
    while True:
        value = random.random()
        print(f"Produced {value}")
        queue.put(value)
        time.sleep(1)


def consumer(queue: Queue):
    while True:
        data = queue.get()
        print(f"Consumed {data}\n")
        time.sleep(1)


q = Queue() tc = Thread(target=consumer, args=(q,))
tp = Thread(target=producer, args=(q,))
tc.start()
tp.start()
```
