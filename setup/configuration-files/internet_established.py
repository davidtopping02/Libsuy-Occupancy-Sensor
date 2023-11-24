import smtplib
from email.mime.text import MIMEText
import subprocess

# Function to get the full ifconfig output
def get_ifconfig_output():
    try:
        # Use ifconfig to get the full output
        result = subprocess.run(['ifconfig'], capture_output=True, text=True)
        output = result.stdout
    except Exception:
        # If an exception occurs, default to a placeholder
        output = 'Unable to retrieve ifconfig output'
    return output

# Function to send email
def send_email(subject, body):

    sender = "raspberrypizero9@gmail.com"
    password = "gdnm xbis szbz khjn"
    recipients = ["topping.david11@gmail.com"]
   
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())

# Get the local ifconfig output
ifconfig_output = get_ifconfig_output()

# Compose the email subject and body
subject = 'Raspberry Pi 1 Connected to the Internet'
body = f'ssh pi@{ifconfig_output}'

# Send the email
send_email(subject, body)

print(body)
