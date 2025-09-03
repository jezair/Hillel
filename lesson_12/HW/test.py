from datetime import *

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
    "shipping": [
        {
            "id": 1,
            "name": "Uklon",
            "cost": 50,
            "time_to_delivery": 5
        },
        {
            "id": 2,
            "name": "Uber",
            "cost": 30,
            "time_to_delivery": 10
        }
    ]
}

print(storage["shipping"][1]["time_to_delivery"] - datetime.now())