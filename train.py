import json
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INTENTS_PATH = os.path.join(BASE_DIR, "app", "intents.json")

with open(INTENTS_PATH, "r", encoding="utf-8") as f:
    intents = json.load(f)["intents"]

patterns = []
tags = []

for intent in intents:
    for pattern in intent["patterns"]:
        patterns.append(pattern.lower())
        tags.append(intent["tag"])

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(patterns)

model = LogisticRegression(max_iter=200)
model.fit(X, tags)

os.makedirs("model", exist_ok=True)

with open("model/chatbot_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("model/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("✅ Model trained successfully!")