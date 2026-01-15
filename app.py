import os
import sys
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
    print("CRITICAL ERROR: GEMINI_API_KEY is missing from environment!")

genai.configure(api_key=api_key)

# 2. SMART MODEL SELECTOR (The Fix)
# We check which model your key actually has access to
def get_working_model():
    print("--- CHECKING AVAILABLE MODELS ---")
    try:
        # Get list of all models available to this API Key
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        print(f"Your Key has access to: {available_models}")

        # Try to find the best one
        preferred_order = ['models/gemini-1.5-flash', 'models/gemini-pro', 'models/gemini-1.0-pro']
        
        for model_name in preferred_order:
            if model_name in available_models:
                print(f"✅ SELECTED MODEL: {model_name}")
                return genai.GenerativeModel(model_name)
        
        # Fallback: Just take the first one found
        if available_models:
            print(f"⚠️ Using fallback model: {available_models[0]}")
            return genai.GenerativeModel(available_models[0])
            
    except Exception as e:
        print(f"Model Check Error: {e}")
    
    # Absolute last resort
    print("❌ Could not verify models. Defaulting to gemini-pro")
    return genai.GenerativeModel('gemini-pro')

# Initialize the model ONCE when server starts
model = get_working_model()

SYSTEM_INSTRUCTION = "You are the Apna Coding AI Assistant. Help users find verified hackathons and jobs. Keep answers short."

@app.route('/')
def home():
    return "Chatbot is Online!"

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message')
        
        # Combine instructions manually
        full_prompt = f"{SYSTEM_INSTRUCTION}\n\nUser: {user_message}"
        
        response = model.generate_content(full_prompt)
        return jsonify({"reply": response.text})
        
    except Exception as e:
        print(f"ERROR DETAILS: {e}")
        return jsonify({"reply": "System Error. Check Render Logs for model list."}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
