import smtplib
from email.mime.text import MIMEText
import subprocess
import time
import sys
import os

# Function to get the full ifconfig output
def get_ifconfig_output():
    try:
        # Use ifconfig to get the full output
        result = subprocess.run(['ifconfig'], capture_output=True, text=True)
        output = result.stdout
        return output
    except subprocess.CalledProcessError as e:
        # If an exception occurs, print the error and return None or handle it appropriately
        print(f"Error running ifconfig: {e}")
        return None

# Function to send email
def send_email(subject, body):
    sender = "raspberrypizero9@gmail.com"
    password = "gdnm xbis szbz khjn"
    recipients = ["topping.david11@gmail.com"]

    # Create an SMTP connection
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()

    # Log in to the SMTP server
    smtp_server.login(sender, password)

    # Compose the email
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender

    # Send the email
    smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Email Sent!")

    # Close the SMTP connection
    smtp_server.quit()

# Get the local ifconfig output
ifconfig_output = get_ifconfig_output()

# Compose the email subject and body
subject = 'Raspberry Pi 1 Connected to the Internet'
body = f'{ifconfig_output}'

# Send the email
send_email(subject, body)

print(body)
