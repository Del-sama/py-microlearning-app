import os
import smtplib
import ssl
import time

from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

PORT = 465
SMTP_SERVER = "smtp.gmail.com"
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')
PASSWORD = os.getenv('PASSWORD')


def main(content):
    """
    Send email
    """
    header, url, body = content
    send_email(header, url, body)


def send_email(header, url, body):
    """
    Set up ssl context, login and send email to receiver

    :Param header: The subject of the email
    :Param url: The resource's url
    :Param body: The body of the email
    """
    msg = EmailMessage()
    msg['Subject'] = header
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    msg.set_content(f"""\
        Hi there!

        Here's your Python Language Reference chapter for the day: {url}
        """
    )

    msg.add_alternative(f"""\
        Hi there!

        <p>
            Here's your Python Language Reference chapter for the day! \
            You can also check this out in \
            <a href="{url}">The Python Library Reference documentation</a>
        </p>

        {body}
        """, subtype='html'
    )

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
        server.login(SENDER_EMAIL, PASSWORD)
        server.send_message(msg)

