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
            "http://vote.cheetos.ee/upvote.php",
            headers=headers,
            data=data,
            proxies=proxy,
            timeout=100
        )
        print(response)

    def send_vote(self, referer, imgId, proxies):
        print("started voting")
        data = {"imgId": imgId, "voteCount": 1, "captcha" :"03AOLTBLQsA50_a235oe7rAfDvBKxAzrrvVVkc0nGcnN9VnFbm-gwUVcRXWMoD4jGYuAX8Cs8515eXEsPU4jNnFscih_nLtiRr8uSCL6GBl2pdsOU_q9GiX0gZv48iCNpGQ999LotmT19k8AG5gc1y-QWZXYeyWTgowl08bsqMS8oRwrS7yq5d_LivBaBriZlycdmitqKiqCTzBe-LFt9XzMRBwhg14XmmsF5UvaUMIwpU24dMH4V-PstktETevV7ZBcRVeKXtTwzJRVwyYGFKeMCECmmLDXymtdQMkiBdJhlLcngFy-_KDx_6gmr1GHUKxSTvQW8K5Xwo"}
        for proxy in proxies:
            user_agent = choice(self.user_agents)["user_agent"]
            headers = {
                "accept": "*/*",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "origin": "https://cheetos.ee",
                "referer": referer,
                "User-Agent": user_agent,
            }
            proxy = {"http": f'http://{proxy}',
                "https": f'https://{proxy}'}
            self.run(self.send_request, headers, data, proxy)
            sleep(5)


voter = CheetosVoter(
    "https://cheetos.ee/avaleht/galerii/images/default-source/est/part5fc206ac2e2b479984a959d46b0a005d?itemIndex=12",
    "Part5",
    "proxy.csv",
    "user_agents.csv",
)

