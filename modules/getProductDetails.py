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


def getProductsDetails(product_url):
    cookies = {
        'T': 'TI169738343084900295082818340723979456530729613097220816710629798709',
        'K-ACTION': 'null',
        '_pxvid': 'd9796d97-6b6e-11ee-afd0-a49108a7912a',
        'AMCV_17EB401053DAF4840A490D4C%40AdobeOrg': '-227196251%7CMCIDTS%7C19646%7CMCMID%7C55982066994611333518228251330304930690%7CMCAAMLH-1697988233%7C12%7CMCAAMB-1697988233%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1697390633s%7CNONE%7CMCAID%7CNONE',
        'at': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImQ2Yjk5NDViLWZmYTEtNGQ5ZC1iZDQyLTFkN2RmZTU4ZGNmYSJ9.eyJleHAiOjE2OTkxMTE0NDcsImlhdCI6MTY5NzM4MzQ0NywiaXNzIjoia2V2bGFyIiwianRpIjoiMmI3YjM4M2EtYWMzZS00NzgxLWJmNjctOGMwNGYwMGZiOWY1IiwidHlwZSI6IkFUIiwiZElkIjoiVEkxNjk3MzgzNDMwODQ5MDAyOTUwODI4MTgzNDA3MjM5Nzk0NTY1MzA3Mjk2MTMwOTcyMjA4MTY3MTA2Mjk3OTg3MDkiLCJrZXZJZCI6IlZJOTZBRTA4MUM5NUQ0NDZFRTk2MzRCRTYyRjBDM0RFNEYiLCJ0SWQiOiJtYXBpIiwidnMiOiJMTyIsInoiOiJIWUQiLCJtIjp0cnVlLCJnZW4iOjR9.hNO4-Vlf6gyxeaVn4GSSHZbtQeZ6mdqGgYAAdvv-SU8',
        'SN': 'VI96AE081C95D446EE9634BE62F0C3DE4F.TOK8A22FDDD7ED2412B891927C543A11BDE.1697383490.LO',
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1"
    }

    requests.packages.urllib3.disable_warnings()

    response = requests.get(product_url, cookies=cookies,
                            headers=headers, verify=False)
    # print(response.content)

    data = {}

    specs_dataset = []

    if response.status_code == 200:
        soup = bs(response.content, 'html.parser')
        divs = soup.find_all(class_="GNDEQ-")

        for div in divs:
            # print(div)
            small_soup = bs(str(div), 'html.parser')

            specificationType = small_soup.find(class_="_4BJ2V+").text

            rows = small_soup.find_all('tr')

            table_data = {}
            for row in rows:
                key = row.find('td', class_='+fFi1w col col-3-12').text
                value = row.find('td', class_='Izz52n col col-9-12').text
                table_data[key] = value
                specs_dataset.append({
                    "key": key,
                    "value": value
                })

            data[specificationType] = table_data

        with open('data/specs.json', 'w') as file:
            json.dump(specs_dataset, file, indent=4)

    return data


# details = getProductsDetails(
#     "https://www.flipkart.com/poco-c51-royal-blue-64-gb/p/itm1e4e8373537a7")

# print(details)
