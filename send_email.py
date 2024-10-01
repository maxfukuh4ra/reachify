
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()
app_password = os.getenv('APP_PASSWORD')
from_email = os.getenv('EMAIL_ADDRESS')

def send_email(to_email, subject, body):
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    try:
        # connect to the Gmail server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # upgrade the connection to secure
        server.login(from_email, app_password)  # use the app password here
        server.sendmail(from_email, to_email, message.as_string())
        server.quit()
        print(f"Email successfully sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}. Error: {e}")