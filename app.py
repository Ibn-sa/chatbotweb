from flask import Flask, send_from_directory, request, jsonify
import os

app = Flask(__name__, static_folder=".")


def build_buddy_reply(message: str, user: dict | None = None) -> str:
    if user is None:
        user = {}
    name = (user.get("name") or "friend").strip() or "friend"

    text = (message or "").lower()
    if not text.strip():
        return "Please type something so I can help you."

    if "hello" in text or "hi" in text:
        return f"Hi {name}! I am Buddy. What would you like to talk about?"

    if any(word in text for word in ["sad", "down", "depressed", "cry"]):
        return (
            "I'm sorry you're feeling sad. It's okay to feel this way. "
            "Try talking to someone you trust, and remember I'm here to listen."
        )

    if any(word in text for word in ["angry", "mad", "frustrated"]):
        return (
            "Your feelings are valid. Maybe take a few deep breaths or a short break. "
            "Do you want to tell me what made you feel this way?"
        )

    if any(word in text for word in ["stressed", "anxious", "nervous", "worried"]):
        return (
            "That sounds stressful. Let's try one small step at a time. "
            "What is one thing we could focus on first?"
        )

    if any(word in text for word in ["happy", "good", "excited", "great"]):
        return (
            "I'm glad you're feeling good! Tell me more about what made you feel this way "
            "so we can celebrate it."
        )

    if "help" in text or "suggest" in text:
        return (
            "Tell me a bit more about what you need help with (study, work, friends, etc.) "
            "and I'll try to give you a simple suggestion."
        )

    return (
        "Thank you for sharing that. I may be simple, but I'm here to listen. "
        "Can you explain a bit more, or tell me how this makes you feel?"
    )


@app.route("/")
def index():
    # Serve the existing index.html from the project root
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "index.html")


@app.route("/api/reply", methods=["POST"])
def api_reply():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")
    user = data.get("user") or {}
    reply = build_buddy_reply(message, user)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)
