import nltk
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


class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"


with open('data/flows.json', 'w') as file:
    json.dump({"flow": "START"}, file, indent=4)


while True:
    user_input = input(
        f"{Colors.GREEN + Colors.BLUE}You:{Colors.RESET} ") or "empty"

    if user_input.lower() == 'help':
        print(f"{Colors.GREEN + Colors.BOLD}Bot:{Colors.RESET} Type '{Colors.BLUE}exit{Colors.RESET}' to end the conversation.")
        continue

    if user_input.lower() == 'exit' or user_input.lower() == "quit":
        print(f"{Colors.GREEN + Colors.BOLD}Bot:{Colors.RESET} Good bye!")
        break

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
                    chatbot_response += f"\nName : {phone['name']}\nPrice : {phone['price']}\nUrl : {phone['url']}"
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
            chatbot_response += json.dumps(data["selected_product"])
        else:
            chatbot_response += f"{spec_query_result['keys']} : {spec_product_name}"

        with open('data/flows.json', 'w') as file:
            json.dump({"flow": "START"}, file, indent=4)

    print(f"{Colors.GREEN + Colors.BOLD}Bot:{Colors.RESET} {chatbot_response}")
