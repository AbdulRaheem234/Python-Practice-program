# pip install pandas schedule twilio
import pandas as pd
import smtplib
from datetime import datetime
from twilio.rest import Client
import schedule
import time
TEXT_FILE = "birthdays.txt"
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
TWILIO_SID = "your_twilio_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"


def send_email(receiver_email, name):
    subject = f"Happy Birthday, {name}!"
    body = f"""
    🎉 Happy Birthday, {name}! 🎂

    Wishing you a fantastic day filled with joy and success!
    Cheers to another amazing year! 🥳

    Best regards,
    Your Python Bot 🤖
    """
    message = f"Subject: {subject}\n\n{body}"
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, receiver_email, message)
    print(f"Email sent to {name} ({receiver_email})")


def send_whatsapp(whatsapp_number, name):
    if not whatsapp_number:
        return
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"🎉 Happy Birthday, {name}! 🎂 Have an amazing day! 🥳",
        from_=TWILIO_WHATSAPP_NUMBER,
        to=f"whatsapp:{whatsapp_number}"
    )
    print(f"WhatsApp message sent to {name} ({whatsapp_number})")


def check_birthdays():
    today = datetime.now().strftime("%m-%d")
    df = pd.read_csv(TEXT_FILE)
    for _, row in df.iterrows():
        name = row["name"]
        birthday = datetime.strptime(
            row["birthday"], "%Y-%m-%d").strftime("%m-%d")
        email = row["email"]
        whatsapp_number = row.get("whatsapp_number", "")
        if today == birthday:
            print(f"🎂 Today is {name}'s birthday!")
            if email:
                send_email(email, name)
            if whatsapp_number:
                send_whatsapp(whatsapp_number, name)


def run_scheduler():
    schedule.every().day.at("09:00").do(check_birthdays)  #
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    print("🎉 Birthday Wisher is running...")
    check_birthdays()
    run_scheduler()
