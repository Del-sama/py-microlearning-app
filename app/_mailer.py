import datetime

import os
import smtplib
import ssl

from email.message import EmailMessage
from dotenv import load_dotenv

from scraper import main as _scraper

load_dotenv()

PORT = 465
SMTP_SERVER = "smtp.gmail.com"
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')
PASSWORD = os.getenv('PASSWORD')

LINKS = _scraper()

START_DATE = datetime.date(2020, 2, 28)


def send_email(content):
    """
    Set up ssl context, login and send email to receiver

    :Param header: The subject of the email
    :Param url: The resource's url
    :Param body: The body of the email
    """
    header, url, body = content

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


if __name__ == "__main__":
    today = datetime.datetime.today().date()
    diff = (today - START_DATE).days
    try:
        send_email(LINKS[diff])
    except IndexError:
        pass
