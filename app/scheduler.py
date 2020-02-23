import datetime

from scraper import main as _scraper
from mailer import main as _send_email

LINKS = _scraper()

START_DATE = datetime.date(2020, 2, 25)

def job(link):
    """
    Run scheduled job
    """
    _send_email(link)


if __name__ == "__main__":
    today = datetime.datetime.today().date()
    diff = (today - START_DATE).days
    try:
        job(LINKS[diff])
    except IndexError:
        pass
