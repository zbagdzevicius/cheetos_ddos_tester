from requests import post
from convert_csv_to_json import csv_to_json
from proxyValidator import ProxyValidator
from threading import Thread
from random import choice
from time import sleep
from scrapperize import crawl_user_agents
from scrapperize import crawl_proxies

user_agents_file = "user_agents.csv"
user_agents = csv_to_json(user_agents_file)

proxies_path_file = "proxies.csv"
proxies = csv_to_json(proxies_path_file)
proxies = [proxy['proxy'] for proxy in proxies]
proxy_validator = ProxyValidator(proxies)
proxies = proxy_validator.validated_proxies


def run(job_fn, *argv):
    arguments = []
    for arg in argv:  
        arguments.append(arg)
    job_thread = Thread(target=job_fn, args=arguments)
    job_thread.start()

def send_request(headers,data,proxy):
    response = post("https://vote.cheetos.ee/upvote.php", headers=headers, data=data, proxies=proxy)
    print(response)

def send_vote(referer, imgId, proxies):
    data = {
        "imgId": imgId
    }
    for proxy in proxies:
        user_agent = choice(user_agents)['user_agent']
        headers = {
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://cheetos.lt",
            "referer": referer,
            "User-Agent": user_agent,
        }
        proxy = {
            "https" : proxy,
        }
        run(send_request, headers, data, proxy)
        sleep(3)





send_vote('https://cheetos.lt/index/galerii/images/librariesprovider3/osalejad/ro%C5%BEyt%C4%97?itemIndex=7','Rožytė 2',proxies)
# send_vote('https://www.cheetos.lt/index/galerii/images/librariesprovider3/osalejad/ranka?itemIndex=21','Ranka',socks_proxies)
# send_vote('https://www.cheetos.lt/index/galerii/images/librariesprovider3/osalejad/ranka?itemIndex=21','Ranka',ssl_proxies)