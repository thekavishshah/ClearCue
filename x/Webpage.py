from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import google.generativeai as genai  # Import the Google Generative AI client

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Ensure the Gemini model and API key are properly configured
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

# Set the API key for the Gemini client
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/explain', methods=['POST'])
def explain():
    user_text = request.form.get('text', '').strip()
    
    if not user_text:
        return jsonify({'error': 'Input text cannot be empty.'}), 400

    prompt = f"Explain the following message in plain literal terms. Clarify sarcasm, tone, or idioms if present:\n\n{user_text}"
    
    try:
        # Use the Gemini client to process the prompt
        
        response = model.generate_content(prompt)
# the SDK gives you the assistant’s reply in `.last`
        explanation = response.text

     
        return jsonify({'explanation': explanation})
    except Exception as e:
        # Log the error for debugging
        print("Error:", str(e))
        return jsonify({'error': 'Failed to process the request.', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5050)