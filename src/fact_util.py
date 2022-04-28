import aiohttp
import asyncio


class FactHandler:
    """
    
    """

    def __init__(self, fact_type='dadjoke', dadjoke_api_endpoint="https://icanhazdadjoke.com/",
                 headers={'User-Agent': 'My Library (https://github.com/Enprogames/Python-Clock/)', 'Accept': 'application/json'}):

        self.fact_type = fact_type
        self.dadjoke_endpoint = dadjoke_api_endpoint
        self.headers = headers
        conn = aiohttp.TCPConnector(limit=None, ttl_dns_cache=300)
        self.session = aiohttp.ClientSession(connector=conn)
        self.joke = ""
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    def cleanup_response_text(self, text):
        """
        Some response text is poorly formatted. For example, it may be littered with newline characters.
        This method attempts to make the text more presentable.
        """
        return text

    async def get_dadjoke_async(self):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(self.dadjoke_endpoint) as response:
                resp_json = await response.json()
                self.joke = self.cleanup_response_text(resp_json['joke'])

    def request_new_dadjoke(self):
        asyncio.run(self.get_dadjoke_async())

    def request_new(self):
        if self.fact_type == 'dadjoke':
            self.request_new_dadjoke()
        elif self.fact_type == 'fact':
            pass

    def get(self):
        return self.joke
