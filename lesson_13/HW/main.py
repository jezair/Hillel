import uuid
from dataclasses import dataclass
import random
import abc
import queue
import threading
import time
from datetime import datetime, timedelta
from typing import Literal

CHECK_ORDER_DELAY = 2

OrderRequestBody = tuple[str, datetime]
DeliveryProvider = Literal["Uklon", "Uber"]
OrderDeliveryStatus = Literal["ongoing", "finished", "archived"]

storage = {
    "delivery": {},  # id: [provider, status, finished_at, archived]
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
    # ...
}


@dataclass
class DeliveryOrder:
    order_name: str
    number: uuid.UUID | None = None


class DeliveryService(abc.ABC):
    def __init__(self, order: DeliveryOrder):
        self._order: DeliveryOrder = order

    @abc.abstractmethod
    def ship(self) -> None:
        """resolve the order with concrete provider"""

    @classmethod
    def _process_delivery(cls) -> None:
        """background process"""

        print("DELIVERY PROCESSING...")

        while True:

            for order_id, value in list(storage["delivery"].items()):
                provider = value["provider"]
                status = value["status"]
                finished_at = value["finished_at"]
                archived = value["archived"]

                if status == "finished" and not archived:
                    if finished_at and (datetime.now() - finished_at).total_seconds() > 10:
                        storage["delivery"][order_id]["archived"] = True
                        storage["delivery"][order_id]["status"] = "archived"
                        print(f"📦 Order {order_id} archived (provider: {provider})")

            filtered = {k: v for k, v in storage["delivery"].items() if v["status"] == "ongoing"}

            for order_id, value in filtered.items():
                if value["status"] == "finished":
                    print(f"\n\t🚚 Order {order_id} is delivered by {value[0]}")

            time.sleep(CHECK_ORDER_DELAY)

    def _ship(self, delay: float):

        def _callback():
            time.sleep(delay)
            storage["delivery"][self._order.number]["status"] = "finished"
            storage["delivery"][self._order.number]["finished_at"] = datetime.now()
            print(f"🚚 DELIVERED {self._order}")

        thread = threading.Thread(target=_callback)
        thread.start()


class Uklon(DeliveryService):
    def ship(self) -> None:
        """ типа этот метод может отличаться от других, потому написан без наследования """
        provider_name = self.__class__.__name__

        self._order.number = uuid.uuid4()

        storage["delivery"][self._order.number] = {
            "provider": provider_name,
            "status": "ongoing",
            "finished_at": None,
            "archived": False,
        }

        delay: float = random.randint(1, 3)

        print(f"\n\t🚚 {provider_name} Shipping {self._order} with {delay} delay")
        self._ship(delay)


class Uber(DeliveryService):
    def ship(self) -> None:
        """ типа этот метод может отличаться от других, потому написан без наследования """
        provider_name = self.__class__.__name__

        self._order.number = uuid.uuid4()

        storage["delivery"][self._order.number] = {
            "provider": provider_name,
            "status": "ongoing",
            "finished_at": None,
            "archived": False,
        }

        delay: float = random.randint(3, 5)
        print(f"\n\t🚚 {provider_name} Shipping {self._order} with {delay} delay")
        self._ship(delay)


class Scheduler:
    def __init__(self):
        self.orders: queue.Queue[OrderRequestBody] = queue.Queue()

    @staticmethod
    def _service_dispatcher() -> type[DeliveryService]:
        random_provider: DeliveryProvider = random.choice(("Uklon", "Uber"))

        match random_provider:
            case "Uklon":
                return Uklon
            case "Uber":
                return Uber

    def ship_order(self, order_name: str) -> None:
        ConcreteDeliveryService: type[DeliveryService] = self._service_dispatcher()
        instance = ConcreteDeliveryService(order=DeliveryOrder(order_name=order_name))
        instance.ship()

    def add_order(self, order: OrderRequestBody) -> None:
        self.orders.put(order)
        print(f"\n\t{order[0]} ADDED FOR PROCESSING")

    def process_orders(self) -> None:
        print("ORDERS PROCESSING...")

        while True:
            order = self.orders.get(True)

            time_to_wait = order[1] - datetime.now()

            if time_to_wait.total_seconds() > 0:
                self.orders.put(order)
                time.sleep(0.5)
            else:
                self.ship_order(order[0])


def main():
    scheduler = Scheduler()
    process_orders_thread = threading.Thread(
        target=scheduler.process_orders, daemon=True
    )
    process_delivery_thread = threading.Thread(
        target=DeliveryService._process_delivery, daemon=True
    )

    process_orders_thread.start()
    process_delivery_thread.start()

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
