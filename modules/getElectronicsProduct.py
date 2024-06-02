from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup as bs
import json


def make_absolute_url(url, domain):
    parsed_url = urlparse(url)

    if parsed_url.netloc:
        return url
    else:
        if domain.endswith('/') and parsed_url.path.startswith('/'):
            absolute_url = domain + parsed_url.path[1:]
        else:
            absolute_url = domain + parsed_url.path

        return absolute_url


def getProducts(product_name):
    cookies = {
        'T': 'TI169738343084900295082818340723979456530729613097220816710629798709',
        'K-ACTION': 'null',
        '_pxvid': 'd9796d97-6b6e-11ee-afd0-a49108a7912a',
        'AMCV_17EB401053DAF4840A490D4C%40AdobeOrg': '-227196251%7CMCIDTS%7C19646%7CMCMID%7C55982066994611333518228251330304930690%7CMCAAMLH-1697988233%7C12%7CMCAAMB-1697988233%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1697390633s%7CNONE%7CMCAID%7CNONE',
        'at': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImQ2Yjk5NDViLWZmYTEtNGQ5ZC1iZDQyLTFkN2RmZTU4ZGNmYSJ9.eyJleHAiOjE2OTkxMTE0NDcsImlhdCI6MTY5NzM4MzQ0NywiaXNzIjoia2V2bGFyIiwianRpIjoiMmI3YjM4M2EtYWMzZS00NzgxLWJmNjctOGMwNGYwMGZiOWY1IiwidHlwZSI6IkFUIiwiZElkIjoiVEkxNjk3MzgzNDMwODQ5MDAyOTUwODI4MTgzNDA3MjM5Nzk0NTY1MzA3Mjk2MTMwOTcyMjA4MTY3MTA2Mjk3OTg3MDkiLCJrZXZJZCI6IlZJOTZBRTA4MUM5NUQ0NDZFRTk2MzRCRTYyRjBDM0RFNEYiLCJ0SWQiOiJtYXBpIiwidnMiOiJMTyIsInoiOiJIWUQiLCJtIjp0cnVlLCJnZW4iOjR9.hNO4-Vlf6gyxeaVn4GSSHZbtQeZ6mdqGgYAAdvv-SU8',
        'SN': 'VI96AE081C95D446EE9634BE62F0C3DE4F.TOK8A22FDDD7ED2412B891927C543A11BDE.1697383490.LO',
    }

    headers = {
        'Host': 'www.flipkart.com',
        'Sec-Ch-Ua': '"Chromium";v="109", "Not_A Brand";v="99"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Full-Version': '"109.0.5414.119"',
        'Sec-Ch-Ua-Arch': '"x86"',
        'Sec-Ch-Ua-Platform': '"Linux"',
        'Sec-Ch-Ua-Platform-Version': '"6.5.9"',
        'Sec-Ch-Ua-Model': '""',
        'Sec-Ch-Ua-Full-Version-List': '"Chromium";v="109.0.5414.119", "Not_A Brand";v="99.0.0.0"',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5414.120 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        # 'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Connection': 'close',
        # 'Cookie': 'T=TI169738343084900295082818340723979456530729613097220816710629798709; K-ACTION=null; _pxvid=d9796d97-6b6e-11ee-afd0-a49108a7912a; AMCV_17EB401053DAF4840A490D4C%40AdobeOrg=-227196251%7CMCIDTS%7C19646%7CMCMID%7C55982066994611333518228251330304930690%7CMCAAMLH-1697988233%7C12%7CMCAAMB-1697988233%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1697390633s%7CNONE%7CMCAID%7CNONE; at=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImQ2Yjk5NDViLWZmYTEtNGQ5ZC1iZDQyLTFkN2RmZTU4ZGNmYSJ9.eyJleHAiOjE2OTkxMTE0NDcsImlhdCI6MTY5NzM4MzQ0NywiaXNzIjoia2V2bGFyIiwianRpIjoiMmI3YjM4M2EtYWMzZS00NzgxLWJmNjctOGMwNGYwMGZiOWY1IiwidHlwZSI6IkFUIiwiZElkIjoiVEkxNjk3MzgzNDMwODQ5MDAyOTUwODI4MTgzNDA3MjM5Nzk0NTY1MzA3Mjk2MTMwOTcyMjA4MTY3MTA2Mjk3OTg3MDkiLCJrZXZJZCI6IlZJOTZBRTA4MUM5NUQ0NDZFRTk2MzRCRTYyRjBDM0RFNEYiLCJ0SWQiOiJtYXBpIiwidnMiOiJMTyIsInoiOiJIWUQiLCJtIjp0cnVlLCJnZW4iOjR9.hNO4-Vlf6gyxeaVn4GSSHZbtQeZ6mdqGgYAAdvv-SU8; SN=VI96AE081C95D446EE9634BE62F0C3DE4F.TOK8A22FDDD7ED2412B891927C543A11BDE.1697383490.LO',
    }

    params = { 
        'q': product_name,
    }

    requests.packages.urllib3.disable_warnings()

    response = requests.get('https://www.flipkart.com/search',
                            params=params, cookies=cookies, headers=headers, verify=False)

    soup = bs(response.content, 'html.parser')
    divs = soup.find_all(class_="cPHDOP")
    # print(len(divs))

    allPhones = []
    for j in range(len(divs)):
        small_html = divs[j]
        # print(small_html)
        small_soup = bs(str(small_html), 'html.parser')

        # print(product_price)

        try:
            product_name = small_soup.find_all(class_="KzDlHZ")
            name = (product_name[0]).text
        except IndexError:
            name = None

        try:
            product_price = small_soup.find_all(class_="Nx9bqj")
            price = (product_price[0]).text

        except IndexError:
            price = None

        try:
            product_urls = small_soup.find_all(class_="CGtC98")
            urls = [link.get('href') for link in product_urls]

            url = make_absolute_url(
                urls[0], "https://www.flipkart.com")
        except IndexError:
            url = None

        if name is not None and price is not None and url is not None:
            allPhones.append({
                "name": name,
                "price": price,
                "url": url,
            })

    return allPhones


# print(json.dumps(getProducts("latest phones"),indent=4))