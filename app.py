import os
from flask import Flask, jsonify, render_template, request, session
from groq import Groq

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "chatbot-secret")


def get_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set")
    return Groq(api_key=api_key)


def build_memory_context():
    history = session.get("history", [])
    if not history:
        return ""
    recent = history[-4:]
    return "\n".join(
        f"User: {item['user']}\nAssistant: {item['assistant']}"
        for item in recent
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    payload = request.get_json(silent=True) or {}
    user_message = (payload.get("message") or "").strip()

    if not user_message:
        return jsonify({"reply": "Please type a message first."}), 400

    memory_context = build_memory_context()
    system_prompt = (
        "You are Ask AI, a calm, thoughtful assistant. Answer briefly, clearly, and helpfully. "
        "If the user seems to want guidance, offer one practical next step."
    )
    if memory_context:
        system_prompt += f"\nUse this recent chat context to stay coherent:\n{memory_context}"

    try:
        client = get_client()
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.7,
            max_tokens=220,
        )
        reply = completion.choices[0].message.content.strip()
    except Exception as exc:
        reply = f"I hit a snag while contacting Groq: {exc}"

    history = session.get("history", [])
    history.append({"user": user_message, "assistant": reply})
    session["history"] = history[-6:]

    return jsonify({"reply": reply})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
