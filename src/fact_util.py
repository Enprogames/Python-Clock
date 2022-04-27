import aiohttp
import asyncio


class JokeHandler:

    def __init__(self, dadjoke_api_endpoint="https://icanhazdadjoke.com/",
                 headers={'User-Agent': 'My Library (https://github.com/Enprogames/Python-Clock/)', 'Accept': 'application/json'}):
        self.dadjoke_endpoint = dadjoke_api_endpoint
        self.headers = headers
        conn = aiohttp.TCPConnector(limit=None, ttl_dns_cache=300)
        self.session = aiohttp.ClientSession(connector=conn)
        self.joke = ""
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    async def get_dadjoke_async(self):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(self.dadjoke_endpoint) as response:
                resp_json = await response.json()
                self.joke = resp_json['joke']

    def get(self):
        asyncio.run(self.get_dadjoke_async())
        return self.joke
