import time
import logging
from TEST import *

class TimerContext:
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.time() - self.start
        logging.info(f"Elapsed: {elapsed:.2f} seconds")

logging.basicConfig(level=logging.INFO)

with TimerContext():
    main()