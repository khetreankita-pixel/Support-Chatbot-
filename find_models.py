import google.generativeai as genai

# PASTE YOUR REAL API KEY HERE
GEMINI_API_KEY = "AIzaSyDo_8tveEXYeHhkkQqJsP_MTgNYFAHT6io"

genai.configure(api_key=GEMINI_API_KEY)

print("------ CHECKING AVAILABLE MODELS ------")
try:
    available_models = []
    for m in genai.list_models():
        # We only want models that can generate text (content)
        if 'generateContent' in m.supported_generation_methods:
            print(f"FOUND: {m.name}")
            available_models.append(m.name)

    if not available_models:
        print("ERROR: No models found! Your API Key might be invalid or restricted.")
    else:
        print("\nSUCCESS! You can use any of the names above.")
        print(f"Recommended: Copy '{available_models[0]}' into your app.py")

except Exception as e:
    print(f"CRITICAL ERROR: {e}")