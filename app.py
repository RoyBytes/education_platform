from flask import Flask, request, jsonify, render_template
from google import genai
import os
import re
from dotenv import load_dotenv
from markupsafe import Markup

load_dotenv()

app = Flask(__name__)

# Create Gemini client (NEW SDK)
GEMINI_API_KEY = "AIzaSyCbxTTkj12xPwTf-H1-jgbF_ICv4gz_a-0"
client = genai.Client(api_key=GEMINI_API_KEY)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    print("Request JSON:", data)
    user_prompt = data.get("prompt", "")

    full_prompt = f"""
{user_prompt}

Please provide:
- some information
- in next line 2 YouTube clickable links
- 2 in next line website clickable links
- 1 PDF link
Each on separate lines.
"""

    try:
        print("Sending prompt to Gemini...")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt
        )
        print("Raw Gemini response:", response)

        # Robust parsing for different SDK response shapes
        answer = None
        if hasattr(response, "text") and response.text:
            answer = response.text
        elif isinstance(response, dict):
            # common dict shapes
            answer = (response.get("content")
                      or (response.get("candidates") or [{}])[0].get("content")
                      or (response.get("outputs") or [{}])[0].get("content"))
        else:
            # try attribute access for candidates/outputs
            candidates = getattr(response, "candidates", None) or getattr(response, "outputs", None)
            if candidates:
                first = candidates[0]
                answer = getattr(first, "content", None) or first.get("content", None)
        if not answer:
            answer = str(response)

        # Make URLs clickable for frontend (send as plain string)
        answer_html = re.sub(
            r'(https?://[^\s]+)',
            r'<a href="\1" target="_blank">\1</a><br><br>',
            answer
        )

        return jsonify({"answer": answer, "html": answer_html})

    except Exception as e:
        print("Gemini error:", repr(e))
        return jsonify({"answer": "Sorry, could not generate a response."})

if __name__ == "__main__":
    app.run(debug=True)
