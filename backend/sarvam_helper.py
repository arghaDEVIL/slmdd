import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SARVAM_API_KEY")

LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "bn": "Bengali",
    "ta": "Tamil",
    "te": "Telugu",
    "mr": "Marathi",
    "gu": "Gujarati",
    "pa": "Punjabi",
    "ml": "Malayalam",
    "kn": "Kannada",
    "or": "Odia",
}


def get_advice(diseases, lang_code):

    language = LANGUAGES.get(lang_code, "English")

    disease_text = ", ".join(diseases)

    prompt = f"""You are an agricultural expert. Provide advice about these plant diseases: {disease_text}

CRITICAL INSTRUCTIONS:
1. Write EVERYTHING in {language} language - including all headings and labels
2. Use clear formatting with emojis
3. Keep it simple for farmers

FORMAT YOUR RESPONSE EXACTLY LIKE THIS:

For each disease:

## [Disease Name in {language}]

### 🦠 [Translate "Cause" to {language}]
[Explain the cause in {language}]

### 🍃 [Translate "Symptoms" to {language}]
[List symptoms in {language}]

### 💊 [Translate "Treatment" to {language}]
[Explain treatment in {language}]

### 🛡️ [Translate "Prevention" to {language}]
[Explain prevention in {language}]

---

After all diseases:

## 🌾 [Translate "Combined Management Strategy" to {language}]
[Management advice in {language}]

## ⚠️ [Translate "Important Notes" to {language}]
[Important warnings in {language}]

Use simple language. Be practical and specific."""

    response = requests.post(
        "https://api.sarvam.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={"model": "sarvam-m", "messages": [{"role": "user", "content": prompt}]},
    )

    data = response.json()

    content = data["choices"][0]["message"]["content"]

    content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()

    return content
