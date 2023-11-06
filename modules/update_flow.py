import json


def updateFlowFile(data):
    with open('data/flows.json', 'w') as file:
        json.dump(data, file, indent=4)
