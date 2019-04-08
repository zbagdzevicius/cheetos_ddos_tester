from proxybroker import Broker
import asyncio
from pprint import pprint
from convert_csv_to_json import csv_to_json
from random import choice
from requests import post

class CheetosVoter:
    def __init__(self, referer, img_id, user_agents_file_path):
        self.referer = referer
        self.data = {"imgId": img_id}
        self.user_agents = csv_to_json(user_agents_file_path)
        proxies = asyncio.Queue()
        broker = Broker(proxies)
        tasks = asyncio.gather(
            broker.find(types=['HTTP', 'HTTPS'], limit=1000000),
            self.show(proxies))
        loop = asyncio.get_event_loop()
        loop.run_until_complete(tasks)


    def send_request(self, proxy):
        user_agent = choice(self.user_agents)["user_agent"]
        headers = {
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://cheetos.lt",
            "referer": self.referer,
            "User-Agent": user_agent,
        }
        try:
            response = post(
                "https://vote.cheetos.ee/upvote.php",
                headers=headers,
                data=self.data,
                proxies=proxy,
                timeout=100,
            )
            print(response)
        except:
            print('bad response')

    async def show(self, proxies):
        while True:
            proxy = await proxies.get()
            if proxy is None: break
            proxy = f'{proxy.host}:{proxy.port}'
            proxy = {"https": f'https://{proxy}'}
            self.send_request(proxy)

voter = CheetosVoter("https://cheetos.lt/index/galerii/images/librariesprovider3/osalejad/ro%C5%BEyt%C4%97?itemIndex=7", "Rožytė 2", "user_agents.csv")