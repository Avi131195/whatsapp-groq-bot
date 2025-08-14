import os
from dotenv import load_dotenv
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import groq

# Load environment variables from .env file
load_dotenv()

# Initialize Groq client with API key
client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))

# Initialize Flask app
app = Flask(__name__)

# Webhook route for incoming WhatsApp messages
@app.route("/whatsapp_webhook", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.values.get('Body', '').strip()
    print(f"📩 Received from WhatsApp: {incoming_msg}")  # For logging

    resp = MessagingResponse()
    msg = resp.message()

    try:
        chat_completion = client.chat.completions.create(
            model="llama3-70b-8192",  # ✅ Make sure this is a supported model
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

# Only used when running locally (not needed on Render)
if __name__ == "__main__":
    app.run(debug=True, port=5000)
