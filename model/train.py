import json
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

with open("../data/intents.json", "r", encoding="utf-8") as f:
    data = json.load(f)

sentences = []
labels = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        sentences.append(pattern.lower())
        labels.append(intent["tag"])

vectorizer = TfidfVectorizer(ngram_range=(1, 2))
X = vectorizer.fit_transform(sentences)

model = LogisticRegression(max_iter=2000)
model.fit(X, labels)

with open("chatbot_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("Model trained successfully")
