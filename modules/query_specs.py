import re
import nltk
import csv
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


nltk.download('punkt')
nltk.download('stopwords')

data = {}
ids = list()

with open('datasets/product_specs_dataset.csv', mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        question = row['Questions']
        key = row['Keys']
        ids.append(row['Id'])

        data[question] = key

questions = list(data.keys())
answers = list(data.values())

stemmer = PorterStemmer()


def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    words = [stemmer.stem(word) for word in words]
    return ' '.join(words)


tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(
    [preprocess_text(q) for q in questions])


def query_specs(input_text):
    input_text = preprocess_text(input_text)
    input_vector = tfidf_vectorizer.transform([input_text])
    cosine_similarities = linear_kernel(input_vector, tfidf_matrix).flatten()
    most_similar_index = cosine_similarities.argsort()[-1]
    return {
        "keys": answers[most_similar_index],
        "Id": ids[most_similar_index]
    }




