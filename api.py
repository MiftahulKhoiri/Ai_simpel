from flask import Flask, request, jsonify, render_template

from core.nlp_engine import NLPEngine
from core.data_manager import add_qa
from core.trainer import train

app = Flask(__name__)

# Load AI sekali (singleton)
ai = NLPEngine()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(force=True)
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "question is required"}), 400

    answer, score = ai.ask_with_score(question)

    if answer:
        return jsonify({
            "answer": answer,
            "confidence": round(score, 3)
        })

    return jsonify({
        "answer": None,
        "confidence": round(score, 3),
        "message": "AI tidak tahu jawabannya"
    })


@app.route("/learn", methods=["POST"])
def learn():
    data = request.get_json(force=True)
    question = data.get("question", "").strip().lower()
    answer = data.get("answer", "").strip()

    if not question or not answer:
        return jsonify({"error": "question and answer required"}), 400

    if add_qa(question, answer):
        train()
        global ai
        ai = NLPEngine()  # reload model

        return jsonify({"status": "learned"})

    return jsonify({"status": "exists"})
