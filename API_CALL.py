from twilio.rest import Client
import os 
from dotenv import load_dotenv
load_dotenv()
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
TO_NUMBER = os.getenv("ALERT_PHONE_NUMBER")

def send_warning(message):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    print(ACCOUNT_SID)

    sms = client.messages.create(
        body=message,
        from_=FROM_NUMBER,
        to=TO_NUMBER
    )

    print("⚠️ Warning sent! SID:", sms.sid)

if __name__ == "__main__":
    warning_msg = "⚠️⚠️⚠️⚠️⚠️🚨 Your Patient Requesting For Help ! ⚠️⚠️⚠️⚠️"
    send_warning(warning_msg)
    
