import aiohttp
import asyncio
import randfacts

TEST_FACT = """
         It's not only writers who can benefit from this free online tool. If you're a programmer who's working on a project where blocks of text are
         needed, this tool can be a great way to get that. It's a good way to test your programming and that the tool being created is working well.

        Above are a few examples of how the random paragraph generator can be beneficial. The best way to see if this random paragraph picker will be
        useful for your intended purposes is to give it a try. Generate a number of paragraphs to see if they are beneficial to your current project.

        If you do find this paragraph tool useful, please do us a favor and let us know how you're using it. It's greatly beneficial for us to know
        the different ways this tool is being used so we can improve it with updates. This is especially true since there are times when the
        generators we create get used in completely unanticipated ways from when we initially created them. If you have the time, please send us a
        quick note on what you'd like to see changed or added to make it better in the future. A paragraph is a coherent block of text, such as a
        group of related sentences that develop a single topic or a coherent part of a larger topic. A blank line contains zero or more non-printing
        characters, such as space or tab, followed by a new line.
        """


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
        self.fact = ""
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    def cleanup_response_text(self, text):
        """
        Some response text is poorly formatted. For example, it may be littered with newline characters.
        This method attempts to make the text more presentable.
        """
        text = text.replace('\n', ' ')  # replace any newlines with spaces
        text = " ".join(text.split())  # remove long periods of space
        return text

    async def get_dadjoke_async(self):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(self.dadjoke_endpoint) as response:
                resp_json = await response.json()
                self.fact = self.cleanup_response_text(resp_json['joke'])

    async def get_fact_async(self, **kwargs):
        new_fact = randfacts.get_fact(filter_enabled=kwargs.get('filter_enabled', True),
                                      only_unsafe=kwargs.get('only_unsafe', False))
        self.fact = self.cleanup_response_text(new_fact)

    def request_new_dadjoke(self, **kwargs):
        asyncio.run(self.get_dadjoke_async(**kwargs))

    def request_new_fact(self, **kwargs):
        asyncio.run(self.get_fact_async(**kwargs))

    def request_new(self):
        if self.fact_type == 'dadjoke':
            self.request_new_dadjoke()
        elif self.fact_type == 'fact':
            self.request_new_fact(filter_enabled=True)

    def get(self):
        return self.fact
