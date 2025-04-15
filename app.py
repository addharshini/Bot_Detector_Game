from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)

def is_bot_response(text):
    bot_keywords = ['I am an AI', 'I\'m a bot', 'As an AI', 'I was trained on', 'I do not understand']
    overly_formal_phrases = ['I apologize for the inconvenience', 'I\'m here to assist you']
    emoji_count = len(re.findall(r'[😀-🙏🚀❤️✨🎉]', text))
    word_count = len(text.split())
    repetition = len(set(text.lower().split())) / (word_count + 1)

    score = 0
    if any(keyword.lower() in text.lower() for keyword in bot_keywords):
        score += 2
    if any(phrase.lower() in text.lower() for phrase in overly_formal_phrases):
        score += 1
    if emoji_count == 0:
        score += 1
    if repetition < 0.5:
        score += 1
    if word_count > 50:
        score += 1

    return score >= 3

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")

    if is_bot_response(message):
        return jsonify({"type": "bot", "result": "🤖 Likely a bot"})
    else:
        return jsonify({"type": "human", "result": "🧑‍💻 Likely a human"})

if __name__ == "__main__":
    app.run(debug=True)




