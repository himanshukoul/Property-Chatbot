import smtplib
from email.message import EmailMessage
import os

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_property_alert(to_email, property_data):
    msg = EmailMessage()
    msg["Subject"] = "New Property Matching Your Preferences!"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email

    body = f"""\
Hi,

A new property has just been listed that matches your preferences!

Location: {property_data['location']}
Price: ₹{property_data['price']}
Bedrooms: {property_data['bedrooms']}
Area: {property_data['area']} sqft
Type: {property_data['property_type']}, {property_data['furnishing']}
Description: {property_data['description'][:300]}...

Login to view more details!

Thanks,
Your Property Bot
"""
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
