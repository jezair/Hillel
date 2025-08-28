import requests

headers = {
    "Authorization": "1"
}


def create_order(order: dict):
    requests.post("/orders", order, headers=headers)