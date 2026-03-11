"""
Greenfield University — College Chatbot
========================================
Deployable on: Vercel · Render · Railway · Heroku · Local

Run locally:
    pip install -r requirements.txt
    python app.py
"""

import json, random, re, math, os
from collections import Counter
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# ── App Setup ─────────────────────────────────────────────────────────────────
app = Flask(__name__, static_folder="public", static_url_path="")
CORS(app)

# ── Load Data ─────────────────────────────────────────────────────────────────
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "college_data.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    _raw = json.load(f)

INTENTS      = _raw["intents"]
COLLEGE_NAME = _raw.get("college_name", "Greenfield University")

# ── NLP Engine ────────────────────────────────────────────────────────────────
STOP_WORDS = {
    "i","me","my","we","our","you","your","he","she","it","they","them",
    "what","which","who","whom","this","that","these","those","am","is",
    "are","was","were","be","been","being","have","has","had","do","does",
    "did","will","would","could","should","may","might","can","a","an",
    "the","and","but","or","nor","so","yet","at","by","for","in","of",
    "on","to","up","as","if","into","with","about","against","between",
    "through","during","before","after","above","below","from","out",
    "off","over","under","then","once","here","there","when","where",
    "how","all","any","both","each","few","more","most","other","some",
    "such","no","not","only","same","than","too","very","just","tell",
    "give","know","need","want","please","get","like"
}

def tokenize(text: str) -> list:
    text = re.sub(r"[^a-z0-9\s]", " ", text.lower())
    return [t for t in text.split() if t not in STOP_WORDS and len(t) > 1]

def tf(tokens: list) -> dict:
    c = Counter(tokens)
    n = len(tokens) or 1
    return {w: v / n for w, v in c.items()}

def cosine(a: dict, b: dict) -> float:
    keys = set(a) & set(b)
    dot  = sum(a[k] * b[k] for k in keys)
    ma   = math.sqrt(sum(v**2 for v in a.values()))
    mb   = math.sqrt(sum(v**2 for v in b.values()))
    return dot / (ma * mb) if ma and mb else 0.0

# Build index once at startup
_index = []
for intent in INTENTS:
    tokens = tokenize(" ".join(intent["patterns"]))
    _index.append((intent["tag"], tf(tokens)))

def predict(text: str, threshold=0.10):
    user_tf = tf(tokenize(text))
    if not user_tf:
        return None, 0.0
    best_tag, best_score = None, 0.0
    for tag, pattern_tf in _index:
        s = cosine(user_tf, pattern_tf)
        if s > best_score:
            best_score, best_tag = s, tag
    return (best_tag, best_score) if best_score >= threshold else (None, best_score)

def get_reply(tag: str) -> str:
    for intent in INTENTS:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])
    return ""

FALLBACKS = [
    "I'm sorry, I didn't understand that. Try asking about:\n• Admissions  • Courses  • Fees\n• Timings     • Faculty  • Exams\n• Placements  • Contact  • Hostel",
    "Could you rephrase that? I can help with admissions, courses, fees, faculty, exams, placements, hostel, and more!",
    "I'm not sure about that one. Contact us at info@greenfield.edu for complex queries.",
]

# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Serve the frontend."""
    return send_from_directory(app.static_folder, "index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    """
    POST /api/chat
    Body : { "message": "your question" }
    Reply: { "response": "...", "intent": "...", "confidence": 0.0–1.0 }
    """
    body = request.get_json(silent=True) or {}
    msg  = body.get("message", "").strip()

    if not msg:
        return jsonify({"error": "No message provided"}), 400

    tag, confidence = predict(msg)

    if tag:
        return jsonify({
            "response":   get_reply(tag),
            "intent":     tag,
            "confidence": round(confidence, 3)
        })

    return jsonify({
        "response":   random.choice(FALLBACKS),
        "intent":     "fallback",
        "confidence": round(confidence, 3)
    })

@app.route("/api/intents", methods=["GET"])
def list_intents():
    """GET /api/intents — list all intent tags."""
    return jsonify({
        "college": COLLEGE_NAME,
        "count":   len(INTENTS),
        "intents": [{"tag": i["tag"], "patterns": i["patterns"]} for i in INTENTS]
    })

@app.route("/api/intents", methods=["POST"])
def add_intent():
    """
    POST /api/intents
    Body: { "tag": "...", "patterns": [...], "responses": [...] }
    Adds a new intent at runtime and saves to disk.
    """
    body = request.get_json(silent=True) or {}
    for field in ("tag", "patterns", "responses"):
        if field not in body:
            return jsonify({"error": f"Missing field: {field}"}), 400

    if any(i["tag"] == body["tag"] for i in INTENTS):
        return jsonify({"error": f"Intent '{body['tag']}' already exists"}), 409

    INTENTS.append(body)
    _index.append((body["tag"], tf(tokenize(" ".join(body["patterns"])))))

    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump({"college_name": COLLEGE_NAME, "intents": INTENTS}, f, indent=2)

    return jsonify({"message": f"Intent '{body['tag']}' added successfully"}), 201

@app.route("/api/health", methods=["GET"])
def health():
    """GET /api/health — uptime check."""
    return jsonify({
        "status":  "ok",
        "college": COLLEGE_NAME,
        "intents": len(INTENTS)
    })

# ── Entry Point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"\n🎓  {COLLEGE_NAME} Chatbot")
    print(f"    http://localhost:{port}\n")
    app.run(debug=False, host="0.0.0.0", port=port)
