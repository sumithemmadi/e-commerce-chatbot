from transformers import BertForQuestionAnswering, BertTokenizer
import torch
import json

from transformers import DistilBertForQuestionAnswering, DistilBertTokenizer

with open("datasets/brands.json", "r") as file:
    data = json.load(file)
phones = data['phones']

model = DistilBertForQuestionAnswering.from_pretrained('distilbert-base-cased-distilled-squad')
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-cased-distilled-squad')

def find_phone_brands(query):
    recognized_brands = []
    for phone in phones:
        if phone.lower() in query.lower():
            recognized_brands.append(phone)
    return recognized_brands if recognized_brands else ["PhoneNotFound"]

def answer_question(question, context):
    inputs = tokenizer.encode_plus(question, context, add_special_tokens=True, return_tensors="pt", max_length=512, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        start_scores = outputs.start_logits
        end_scores = outputs.end_logits

    start_index = torch.argmax(start_scores)
    end_index = torch.argmax(end_scores) + 1

    input_ids = inputs["input_ids"].tolist()[0]
    answer = tokenizer.decode(input_ids[start_index:end_index], skip_special_tokens=True)

    return answer

def getPhonesFromQuery(user_input):
    recognized_brands = find_phone_brands(user_input)
    if "PhoneNotFound" in recognized_brands:
        return "PhoneNotFound"
    
    phone_brands = ", ".join(recognized_brands)
    result = answer_question(user_input, phone_brands)
    return recognized_brands, result
