import queue
import threading
import time
from datetime import datetime, timedelta
from random import randint

OrderRequestBody = tuple[str, datetime]


storage = {
    "users": [],
    "dishes": [
        {
            "id": 1,
            "name": "Salad",
            "value": 1099,
            "restaurant": "Silpo",
        },
        {
            "id": 2,
            "name": "Soda",
            "value": 199,
            "restaurant": "Silpo",
        },
        {
            "id": 3,
            "name": "Pizza",
            "value": 599,
            "restaurant": "Kvadrat",
        },
    ],
    "deliverers": [
        {
            "id": 1,
            "name": "Uklon",
            "cost": 50,
            "time_to_delivery": 5,
            "delivery_count": 0
        },
        {
            "id": 2,
            "name": "Uber",
            "cost": 30,
            "time_to_delivery": 3,
            "delivery_count": 0
        }
    ]
}


class Scheduler:
    def __init__(self):
        self.process_queue_orders: queue.Queue[OrderRequestBody] = queue.Queue()
        self.delivery_queue_orders: queue.Queue[OrderRequestBody] = queue.Queue()

    def process_orders(self) -> None:
        print("SCHEDULER PROCESSING...")

        while True:
            order = self.process_queue_orders.get(True)

            time_to_wait = order[1] - datetime.now()

            if time_to_wait.total_seconds() > 0:
                self.process_queue_orders.put(order)
                time.sleep(0.5)
            else:
                self.delivery_queue_orders.put(order)
                print(f"\n\t{order[0]} SENT TO SHIPPING DEPARTMENT")

    def delivery_orders(self) -> None:
        print("SCHEDULER PROCESSING...")

        while True:
            order = self.delivery_queue_orders.get(True)
            deliverer = min(storage["deliverers"], key=lambda d: d["delivery_count"])
            deliverer["delivery_count"] += 1

            delivery_time = deliverer["time_to_delivery"]

            print(f"{order[0]} DELIVERY STARTED with {deliverer['name']} (takes {deliverer['time_to_delivery']} sec)")

            time.sleep(delivery_time)
            print(f"\n\t{order[0]} SHIPPING IS DONE by Uber")

    def add_order(self, order: OrderRequestBody) -> None:
        self.process_queue_orders.put(order)
        print(f"\n\t{order[0]} ADDED FOR PROCESSING")


def main():
    scheduler = Scheduler()
    thread_1 = threading.Thread(target=scheduler.process_orders, daemon=True)
    thread_1.start()
    thread_2 = threading.Thread(target=scheduler.delivery_orders, daemon=True)
    thread_2.start()

    # user input:
    # A 5 (in 5 days)
    # B 3 (in 3 days)
    while True:
        order_details = input("Enter order details: ")
        data = order_details.split(" ")
        order_name = data[0]
        delay = datetime.now() + timedelta(seconds=int(data[1]))
        scheduler.add_order(order=(order_name, delay))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        raise SystemExit(0)
