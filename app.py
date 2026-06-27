import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# 🔑 1. Groq API Key aur Client Configuration
OPENAI_API_KEY = "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"

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

company_context = ""


# 📂 2. Data Loading Function
def initialize_bot():
    global client, company_context
    try:
        if os.path.exists("company_data.txt"):
            with open("company_data.txt", "r", encoding="utf-8") as f:
                company_context = f.read()
            print("Company data loaded successfully!")
        else:
            print("Warning: company_data.txt not found!")

        if client:
            print("Groq Client is ready and connected!")

    except Exception as e:
        print(f"Init Error: {e}")


# 🌐 3. Flask Routes
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    global client, company_context
    if not client:
        return jsonify({"response": "System Error: Groq client is not initialized."})

    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"response": "Please type a message."})

    try:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an official AI assistant for Conzummate. Tone: polite and professional. "
                    "Language rule: Match the user's language. If the user speaks English, respond in professional English. "
                    "If the user speaks Roman Urdu, respond in simple, natural Pakistani-style Roman Urdu mixed with English technical terms. "
                    "Strictly NEVER use Shudh Hindi words like 'pramukh', 'pradan', 'prabhavi', 'vishesh', 'shamil', 'mahir', 'badi umar ki'.\n\n"
                    "Greeting rule: Only say 'Assalamu alaikum!' or 'Hello' if the user explicitly greets you first (like 'hlo', 'hi', 'helo'). Do not start business answers with a greeting if the user is asking a direct question.\n\n"
                    "Examples:\n"
                    "User: hlo\n"
                    "Assistant: Assalamu alaikum! Main aapki kya help kar sakta hoon?\n\n"
                    "User: conzummate can offer web development\n"
                    "Assistant: Yes, Conzummate is an expert web development company that provides high-quality web applications using frameworks like Flask and React. Our services include custom web development, e-commerce platforms (like ShopEasy), and frontend/backend solutions.\n\n"
                    f"Context:\n{company_context}"

                )
            },
            {"role": "user", "content": user_input}
        ]

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.0
        )

        reply = response.choices[0].message.content
        return jsonify({"response": reply})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

# 🏁 4. App Start
if __name__ == "__main__":
    initialize_bot()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)