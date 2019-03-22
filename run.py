from requests import post
from convert_csv_to_json import csv_to_json
from proxyValidator import ProxyValidator
from threading import Thread
from random import choice
from time import sleep
from scrapperize import crawl_user_agents
from scrapperize import crawl_proxies
import json

proxies_path = "proxies.csv"
with open(proxies_path) as proxies_file:
    proxies_file_data = json.loads(proxies_file)
user_agents = "user_agents.csv"
with open(proxies_path) as user_agents_file:
    user_agents_data = json.loads(user_agents_file)

print(proxies_file_data)

def run(job_fn, *argv):
    arguments = []
    for arg in argv:  
        arguments.append(arg)
    job_thread = Thread(target=job_fn, args=arguments)
    job_thread.start()

def send_request(headers,data,proxy):
    response = post("https://cheetos.lt/upvote.php", headers=headers, data=data, proxies=proxy)
    print(response)

def send_vote(referer, imgId, proxies):
    proxy_type = proxies[0].keys()
    is_socks_proxy = False
    if proxy_type == "socks5":
        is_socks_proxy = True
    
    data = {
        "imgId": imgId
    }

    for proxy in proxies:
        user_agent = choice(user_agents)['user_agent']
        headers = {
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://www.cheetos.lt",
            "referer": referer,
            "User-Agent": user_agent,
        }
        if is_socks_proxy:
            proxy = {
                "https" : f"socks5://{proxy['socks5']}",
            }
        else:
            proxy = {
                "https" : proxy['http'],
            }
        run(send_request, headers, data, proxy)
        sleep(3)





send_vote('https://www.cheetos.lt/index/galerii/images/librariesprovider3/osalejad/ranka?itemIndex=21','Ranka',new_proxies)
# send_vote('https://www.cheetos.lt/index/galerii/images/librariesprovider3/osalejad/ranka?itemIndex=21','Ranka',socks_proxies)
# send_vote('https://www.cheetos.lt/index/galerii/images/librariesprovider3/osalejad/ranka?itemIndex=21','Ranka',ssl_proxies)