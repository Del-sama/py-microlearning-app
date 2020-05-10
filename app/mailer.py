import datetime
import logging
import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from dotenv import load_dotenv

from db import query_db
from db import save_to_db
from scraper import main as _scrape_link

load_dotenv()
logger = logging.getLogger(__name__)

SENDER_EMAIL = os.getenv('SENDER_EMAIL')
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')

START_DATE = datetime.date(2020, 5, 10)


def send_email(content): # pylint: disable = redefined-outer-name
    """
    Set up SendGrid and send email to receiver

    :Param content: Tuple of (header, url, body)
    """
    header, url, body = content

    message_body = f"""\
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
        html_content=message_body
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
    idx = (today - START_DATE).days
    try:
        content = _scrape_link(idx)
    except IndexError:
        logger.warning('No link at index: %d', idx)
    else:
        save_to_db(content)

    # List indices start at 0, but incremental database primary keys start at 1
    to_send = query_db(idx+1)
    if to_send:
        send_email(to_send)
