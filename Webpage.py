from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Configure your OpenAI key here
openai.api_key = "sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/explain', methods=['POST'])
def explain():
    user_text = request.form['text']
    
    prompt = f"Explain the following message in plain literal terms. Clarify sarcasm, tone, or idioms if present:\n\n{user_text}"
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    
    explanation = response.choices[0].message['content']
    return jsonify({'explanation': explanation})

if __name__ == '__main__':
    app.run(debug=True)