import os
from dotenv import load_dotenv
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import groq

load_dotenv()  # Load .env file

client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))

app = Flask(__name__)

# ✅ NEW: Home route for GET testing
@app.route("/", methods=["GET"])
def home():
    return "✅ App is live!"

@app.route("/whatsapp_webhook", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()
    msg = resp.message()

    try:
        print("📩 Incoming message:", incoming_msg)  # For logs
        chat_completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": incoming_msg}
            ]
        )
        ai_reply = chat_completion.choices[0].message.content.strip()
        msg.body(ai_reply)
    except Exception as e:
        print("❌ Groq API Error:", repr(e))
        msg.body("⚠️ Sorry, I couldn't process your request. Try again later.")

    return str(resp)

# Only used for local testing
if __name__ == "__main__":
    app.run(debug=True, port=5000)
