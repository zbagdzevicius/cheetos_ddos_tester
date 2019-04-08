from convert_csv_to_json import csv_to_json

proxies_json = csv_to_json('proxies5.csv')
proxies = [proxy["proxy"] for proxy in proxies_json]
for proxy in proxies:
    splitted_proxy = proxy.split(':')
    proxy_credentials = f'{splitted_proxy[2]}:{splitted_proxy[3]}'
    proxy_port = f'{splitted_proxy[0]}:{splitted_proxy[1]}'
    print(f'{proxy_credentials}@{proxy_port}')