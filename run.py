from requests import post
from convert_csv_to_json import csv_to_json
from proxyValidator import ProxyValidator
from threading import Thread, Event
from random import choice
from time import sleep
from scrapperize import crawl_user_agents
from scrapperize import crawl_proxies

crawl_proxies()


class CheetosVoter:
    def __init__(self, referer, img_id, proxies_file_path, user_agents_file_path):
        self.user_agents = csv_to_json(user_agents_file_path)
        proxies_json = csv_to_json(proxies_file_path)
        # proxies = self.__validated_proxies(proxies_json)
        proxies = [proxy["proxy"] for proxy in proxies_json]
        # print(f"validated proxies:{proxies}")
        self.send_vote(referer, img_id, proxies)

    def __validated_proxies(self, proxies):
        proxies = [proxy["proxy"] for proxy in proxies]
        proxy_validator = ProxyValidator()
        proxy_validator.validate_proxies(proxies)
        proxies = proxy_validator.validated_proxies
        return proxies

    @staticmethod
    def run(job_fn, *argv):
        arguments = []
        for arg in argv:
            arguments.append(arg)
        job_thread = Thread(target=job_fn, args=arguments)
        job_thread.start()

    @staticmethod
    def send_request(headers, data, proxy):
        response = post(
            "https://vote.cheetos.ee/upvote.php",
            headers=headers,
            data=data,
            proxies=proxy,
            # timeout=25
        )
        print(response)

    def send_vote(self, referer, imgId, proxies):
        print("started voting")
        data = {"imgId": imgId}
        for proxy in proxies:
            user_agent = choice(self.user_agents)["user_agent"]
            headers = {
                "accept": "*/*",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "origin": "https://cheetos.lt",
                "referer": referer,
                "User-Agent": user_agent,
            }
            proxy = {"https": proxy}
            self.run(self.send_request, headers, data, proxy)
            sleep(0.1)


voter = CheetosVoter(
    "https://cheetos.lt/index/galerii/images/librariesprovider3/osalejad/ro%C5%BEyt%C4%97?itemIndex=7",
    "Rožytė 2",
    "proxies.csv",
    "user_agents.csv",
)

