
import json

def access_product(data, path):
    keys = path.split('/')
    result = data
    try:
        for key in keys:
            result = result[key]
        return result
    except (KeyError, TypeError):
        return None


with open('data/flows.json', 'r') as file:
    data = json.load(file)
# print(data)
print(access_product(
    data, "selected_product/specs/Memory & Storage Features"))
