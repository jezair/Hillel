## aiohttp usage

```python
import asyncio
from typing import Generator
import aiohttp

BASE_URL = "https://pokeapi.co/api/v2/pokemon"
ids: Generator[int, None, None] = [i for i in range(1, 101)]

async def fetch_pokemon(session, id: int):
    url = f"{BASE_URL}/{id}"

    async with session.get(url) as response:
        data = await response.json()
        # print(f"{id}: {response.status}")
    return data


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_pokemon(session, id) for id in ids]
        results = await asyncio.gather(*tasks)
        print(len(results), "results")

asyncio.run(main())
```

## socket client
```python
import socket

# create socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("google.com", 80))

request = b"GET / HTTP/1.1\r\nHost: exmple.com\r\n\r\n"


data = "\n\n"
data = b"\n\n"

s.sendall(request)


response = s.recv(4096)

print(response.decode())
```


## socket server

```python
import socket

# create socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 8082))
s.listen()

print("Started server on 8080 port...")

conn, addr = s.accept()
print(f"Connection from {addr}")

data = conn.recv(1024)
print(f"Received: {data.decode()}")

conn.close()
s.close()
```
