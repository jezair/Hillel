"""
EDA (event driven architecture)


producer / consumer
"""

import random
import time
from multiprocessing import Process
from queue import Queue
from threading import Thread


def foo():
    while True:
        time.sleep(2)


if __name__ == "__main__":
    t = Process(target=foo)
    t.start()
