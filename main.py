import os
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get credentials from .env
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_number = os.getenv('TWILIO_PHONE_NUMBER')   # Already has 'whatsapp:'
your_number = os.getenv('YOUR_PHONE_NUMBER')       # Already has 'whatsapp:'

# Initialize Twilio client
client = Client(account_sid, auth_token)

# Send message
message = client.messages.create(
    body="Hello from Python using Twilio WhatsApp Sandbox!",
    from_=twilio_number,
    to=your_number
)

print(f"✅ Message sent successfully! SID: {message.sid}")
