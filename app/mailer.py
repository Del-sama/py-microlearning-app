import datetime
import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from dotenv import load_dotenv

from scraper import main as _scrape_link

load_dotenv()

SENDER_EMAIL = os.getenv('SENDER_EMAIL')
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')

START_DATE = datetime.date(2020, 3, 6)


def send_email(content):
    """
    Set up sendgrid and send email to receiver

    :Param content: Tuple of (header, url, body)
    """
    header, url, body = content

    content = f"""\
        Hi there!

        <p>
            Here's your Python Language Reference chapter for the day! \
            You can also check this out in \
            <a href="{url}">The Python Library Reference documentation</a>
        </p>

        {body}
        """

    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=RECEIVER_EMAIL,
        subject=header,
        html_content=content
    )

    try:
        sendgrid = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sendgrid.send(message)
        assert response.status_code == 202 or response.status_code == 200, \
            "Message was not sent successfully"
    except Exception as e:
        raise e

if __name__ == "__main__":
    today = datetime.datetime.today().date()
    diff = (today - START_DATE).days
    link = _scrape_link(diff)
    try:
        send_email(link)
    except IndexError:
        # The App stops sending emails once we’ve run through
        # the 10 chapters of the documentation
        pass
