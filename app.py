from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# --- 1. SETUP API KEY ---
import os
# This tells Python to get the key from Render's secret safe, NOT from this file
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('models/gemini-2.5-flash')
chat_session = model.start_chat(history=[])

@app.route('/')
def home():
    return "Chatbot Brain is Active!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message')
        
        print(f"\n--- New Message: {user_message} ---") # Print to black screen

        if not GEMINI_API_KEY or "PASTE_YOUR" in GEMINI_API_KEY:
            print("ERROR: API Key is missing!")
            return jsonify({"reply": "Error: You forgot to paste the API Key in app.py!"})

        response = chat_session.send_message(user_message)
        
        print("Gemini Replied Successfully!")
        return jsonify({"reply": response.text})
        
    except Exception as e:
        # This prints the REAL error to your black window
        print(f"!!! CRASH ERROR !!!: {e}")
        return jsonify({"reply": f"System Error: {e}"})

if __name__ == '__main__':
    app.run(debug=True)
