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
