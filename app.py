import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# 1. Load secrets from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# 2. Configure API with the secure key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("CRITICAL ERROR: No API Key found in .env file!")

genai.configure(api_key=api_key)

# 3. Define the System Persona (The "Brain")
SYSTEM_INSTRUCTION = """
You are the Apna Coding AI Assistant.
Your goal is to help developers find verified hackathons and jobs.
Always mention that our opportunities are "Verified Safe".
Keep answers short, professional, and helpful.
"""

@app.route('/')
def home():
    return "Secure Chatbot Brain is Active!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message')
        
        print(f"\n--- User Asked: {user_message} ---")

        # 4. FIX: Initialize model INSIDE the function 
        # This prevents "Shared History" bugs between different users.
      model = genai.GenerativeModel(
    model_name='gemini-pro'  # <--- This is the stable version
)
        )
        
        # Send the message
       # We manually combine the "Brain" and the "User Message."
full_prompt = SYSTEM_INSTRUCTION + "\n\nUser: " + user_message
response = model.generate_content(full_prompt)
        
        print("Bot Replied Successfully")
        return jsonify({"reply": response.text})
        
    except Exception as e:
        print(f"ERROR: {e}")
        # Send a polite error to the user, not the crash report
        return jsonify({"reply": "I'm having trouble connecting to the brain right now. Please try again."}), 500

if __name__ == '__main__':
    # Use the PORT environment variable for Render deployment
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
