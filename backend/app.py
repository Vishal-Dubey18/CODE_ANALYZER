from flask import Flask, request, jsonify
from flask_cors import CORS
from together import Together

# ✅ Replace this with your actual Together API key
client = Together(api_key="tgp_v1_yw64JIu21pxO3Tz-4hW9Rm2N6riYzkKE_KfJWo9KfNE")

app = Flask(__name__)
CORS(app)

@app.route("/analyze", methods=["POST"])
def analyze_code():
    try:
        data = request.get_json()
        code = data.get("code", "")
        if not code:
            return jsonify({"error": "Code is required"}), 400

        # Language-independent prompt
        prompt = f"""
You are a senior software engineer.
Analyze and explain the following code written in ANY programming language in proper manner:

1. What does the code do?
2. Explain its logic clearly for a beginner.
3. What is the time and space complexity?
4. Suggest any improvements or optimizations if possible.

Code:
{code}
"""

        stream = client.chat.completions.create(
            model="mistralai/Mixtral-8x7b-Instruct-v0.1",
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            max_tokens=400,
        )

        result = ""
        for chunk in stream:
            if hasattr(chunk, 'choices') and chunk.choices:
                choice = chunk.choices[0]
                if hasattr(choice, 'delta') and hasattr(choice.delta, 'content'):
                    result += choice.delta.content

        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)