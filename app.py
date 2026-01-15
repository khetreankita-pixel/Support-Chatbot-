import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)
CORS(app)

# 1. SETUP API KEY
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not found in environment variables")

genai.configure(api_key=api_key)

# 2. DEFINE SYSTEM INSTRUCTIONS
SYSTEM_INSTRUCTION = """
You are the Apna Coding AI Assistant.
Your goal is to help developers find verified hackathons and jobs.
Always mention that our opportunities are "Verified Safe".
Keep answers short, professional, and helpful.
"""

@app.route('/')
def home():
    return "Chatbot Brain is Active!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message')
        
        print(f"\n--- User Asked: {user_message} ---")

        # 3. USE GEMINI-PRO (Stable Model)
        # We initialize the model inside the function to avoid user history conflicts
        model = genai.GenerativeModel('gemini-pro')
        
        # Manually combine instructions with user message
        full_prompt = f"{SYSTEM_INSTRUCTION}\n\nUser: {user_message}"
        
        response = model.generate_content(full_prompt)
        
        print("Bot Replied Successfully")
        return jsonify({"reply": response.text})
        
    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"reply": "I'm having trouble connecting right now. Please try again."}), 500

if __name__ == '__main__':
    # Use the PORT environment variable for Render deployment
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
