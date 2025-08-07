from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

import re
from markupsafe import Markup

app = Flask(__name__)

# Set your actual API key here
GEMINI_API_KEY = "AIzaSyD5exJb9RlDhhqcstkNwSP4PzwXs-YA4AE"
genai.configure(api_key=GEMINI_API_KEY)

# Load the Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])



@app.route('/ask', methods=['POST'])

def ask():
    data = request.json
    user_prompt = data.get("prompt", "")

    # Enhance the prompt to request links clearly
    full_prompt = f"""{user_prompt}
Please also provide 2 YouTube links, 2 website links and some pdf link also, each on separate lines."""

    try:
        response = model.generate_content(full_prompt)
        answer = response.text

        # Convert URLs into clickable <a> tags with line breaks
        answer = re.sub(
            r'(https?://[^\s]+)',
            r'<a href="\1" target="_blank">\1</a><br><br>',
            answer
        )

        return jsonify({"answer": Markup(answer)})

    except Exception as e:
        print("Gemini error:", e)
        return jsonify({"answer": "Sorry, could not generate a response."})

if __name__ == '__main__':
    app.run(debug=True)