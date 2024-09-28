from flask import Flask, request, jsonify
import re
import nltk
import csv
from modules.getElectronicsProduct import getProducts
from modules.getPhoneBrand import getPhonesFromQuery
from modules.getProductDetails import getProductsDetails
from modules.query_specs import query_specs
import json

nltk.download('punkt')
nltk.download('stopwords')


def access_product(data, path):
    keys = path.split('/')
    result = data
    try:
        for key in keys:
            result = result[key]
        return result
    except (KeyError, TypeError):
        return None


with open('data/flows.json', 'w') as file:
    json.dump({"flow": "START"}, file, indent=4)

app = Flask(__name__)


@app.route('/api', methods=['POST'])
def send_message():

    data = request.get_json()
    if 'phoneNumber' in data and 'message' in data:
        phone_number = data['phoneNumber']
        message = data['message']
        user_input = message
        print(f"Sending message '{message}' to {phone_number}")

        with open('data/flows.json', 'r') as file:
            data = json.load(file)

        chatbot_response = ""

        if (data["flow"] == "START" and chatbot_response == ""):
            phone = getPhonesFromQuery(user_input)

            if (phone == "PhoneNotFound"):
                result = getProducts("latest phones")
            else:
                result = getProducts(phone)
            data["products_list"] = result
            for i, phone in enumerate(result, 1):
                chatbot_response += f"\n{i}. {phone['name']}\t{phone['price']}"

            data["flow"] = "SELECT"

            with open('data/flows.json', 'w') as file:
                json.dump(data, file, indent=4)

        if (data["flow"] == "SELECT" and chatbot_response == ""):
            if "products_list" in data:
                if user_input.isdigit():
                    index = int(user_input) - 1
                    if 0 <= index < len(data["products_list"]):
                        phone = data["products_list"][index]
                        chatbot_response += f"\nName : {phone['name']}\nPrice : {
                            phone['price']}\nUrl : {phone['url']}"
                        data["flow"] = "QUERY_PROCUCT"
                        data["selected_product"] = phone
                        product_specs = getProductsDetails(phone['url'])

                        data["selected_product"]["specs"] = product_specs

                        with open('data/flows.json', 'w') as file:
                            json.dump(data, file, indent=4)

                    else:
                        chatbot_response += f"Enter valid number"
                else:
                    chatbot_response += f"Please select a phone by entering the corresponding number from the menu above."
            else:
                chatbot_response += f"Please select a product"
                with open('data/flows.json', 'w') as file:
                    json.dump({"flow": "START"}, file, indent=4)

        if (data["flow"] == "QUERY_PROCUCT" and chatbot_response == ""):

            spec_query_result = query_specs(user_input)
            spec_product_name = access_product(data, spec_query_result["Id"])
            if (spec_query_result['keys'] == "ALL"):
                chatbot_response += json.dumps(
                    data["selected_product"], ascii=False, indent=3)
            else:
                chatbot_response += f"{
                    spec_query_result['keys']} : {spec_product_name}"

        return jsonify({'message': chatbot_response})

    else:
        return jsonify({'message': 'Something wrong'})


if __name__ == '__main__':
    app.run(debug=True)
