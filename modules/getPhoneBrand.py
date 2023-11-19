from transformers import BertForQuestionAnswering, BertTokenizer
import torch
import json

with open("datasets/brands.json", "r") as file:
    data = json.load(file)
phones = data['phones']

model = BertForQuestionAnswering.from_pretrained(
    'bert-large-uncased-whole-word-masking-finetuned-squad')
tokenizer = BertTokenizer.from_pretrained(
    'bert-large-uncased-whole-word-masking-finetuned-squad')


def find_phone_brand(query):
    for phone in phones:
        if phone.lower() in query.lower():
            return phone
    return "PhoneNotFound"


def answer_question(question, context):
    inputs = tokenizer.encode_plus(
        question, context, add_special_tokens=True, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
        start_scores = outputs.start_logits
        end_scores = outputs.end_logits

    start_index = torch.argmax(start_scores)
    end_index = torch.argmax(end_scores) + 1

    input_ids = inputs["input_ids"].tolist()[0]
    answer = tokenizer.convert_tokens_to_string(
        tokenizer.convert_ids_to_tokens(input_ids[start_index:end_index]))

    return answer


def getPhoneFromQuery(user_input):
    phone_brands = ", ".join(phones)
    result = answer_question(user_input, phone_brands)
    phone_brand = find_phone_brand(result)
    return phone_brand
