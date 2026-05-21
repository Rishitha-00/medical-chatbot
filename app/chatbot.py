import requests
import json
import random
import os

OLLAMA_URL = "http://localhost:11434/api/generate"

# Load intents
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INTENTS_PATH = os.path.join(BASE_DIR, "intents.json")

with open(INTENTS_PATH, "r", encoding="utf-8") as file:
    intents = json.load(file)


# 🚨 Emergency Detection
def check_emergency(text):
    text = text.lower()

    if "pain" in text and "left arm" in text:
        return True
    if "severe chest pain" in text:
        return True
    if "can't breathe" in text or "cannot breathe" in text:
        return True
    if "unconscious" in text or "seizure" in text:
        return True
    if "heavy bleeding" in text:
        return True

    return False


# 🤖 Intent Matching
def get_intent(user_input):
    user_input_lower = user_input.lower()
    user_words = user_input_lower.split()

    # ✅ Exact match
    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            if pattern.lower() in user_input_lower:
                return intent["tag"], random.choice(intent["responses"])

    # ✅ Score-based match
    best_match = None
    best_score = 0

    for intent in intents["intents"]:
        for pattern in intent["patterns"]:
            pattern_words = pattern.lower().split()
            score = sum(1 for word in pattern_words if word in user_words)

            if score > best_score:
                best_score = score
                best_match = intent

    if best_score >= 2:
        return best_match["tag"], random.choice(best_match["responses"])

    return None, None


# 💬 Main Function
def get_response(user_input: str):
    try:
        # 🚨 Emergency first
        if check_emergency(user_input):
            return {
                "tag": "emergency",
                "reply": "⚠️ This may be a medical emergency. Please seek immediate medical help."
            }

        tag, intent_reply = get_intent(user_input)

        if tag:
            context = f"Symptom category: {tag}. Info: {intent_reply}"
        else:
            context = "General symptoms"

        # 🧠 STRICT PROMPT (NO HALLUCINATION)
        prompt = f"""
You are a medical assistant.

STRICT RULES:
- Answer ONLY about the user's symptoms
- DO NOT add stories or examples
- DO NOT mention multiple diseases
- DO NOT mention rare diseases
- Give exactly 3 to 4 sentences
- Keep answer short and relevant

Context: {context}

User: {user_input}
Assistant:
"""

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "phi:latest",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 80
                }
            },
            timeout=60
        )

        result = response.json()
        ai_reply = result.get("response", "").strip()

        # ✂️ Remove extra paragraphs
        ai_reply = ai_reply.split("\n")[0]

        # 🚨 Remove unwanted content
        bad_phrases = [
            "in a hospital",
            "patients",
            "wards",
            "case study"
        ]

        for phrase in bad_phrases:
            if phrase in ai_reply.lower():
                ai_reply = "These symptoms may be related to a common condition. Please consult a healthcare professional for proper evaluation."
                break

        # 🚨 Remove dangerous disease mentions
        bad_words = ["cancer", "tumor", "carcinoma"]
        for word in bad_words:
            if word in ai_reply.lower():
                ai_reply = "These symptoms may be due to common issues like infection or irritation. Please consult a healthcare professional."
                break

        # ✅ Ensure proper ending
        if not ai_reply.endswith((".", "!", "?")):
            ai_reply += " Please consult a healthcare professional."

        return {
            "tag": tag if tag else "general",
            "reply": ai_reply
        }

    except Exception as e:
        print("ERROR:", e)
        return {
            "tag": "error",
            "reply": "⚠️ Unable to connect to AI model."
        }