import re

import requests

from bs4 import BeautifulSoup

BASE_URL = 'https://docs.python.org/3/reference/'


def main(idx):
    """
    Scrape base url, extract links and save to db

    :Param idx: index of link to parsed
    :Return: parsed content
    """
    content = _scraper(BASE_URL)
    links = content.findAll(href=_has_no_hashtag)

    # We want to get only the 10 chapters of the reference
    start = 17
    end = -14
    links = links[start:end]

    result = _handle_link(links[idx])
    return result


def _has_no_hashtag(href):
    """
    Remove sub chapters

    :Param href: tags with the `href` attribute
    :Return: True if `href` exists and does not contain a hashtag
             else return False
    """
    return href and not re.compile("#").search(href)


def _handle_link(link):
    """
    Scrape and parse link

    :Param link: link to be parsed
    :Return: tuple of (header, url, body)
    """
    url = f"{BASE_URL}{link.get('href')}"
    content = _scraper(url)

    permalink = content.findChildren("a", {"class": "headerlink"})
    _decompose(permalink)

    header = content.find('h1').text.lstrip('0123456789. ')
    body = content.find("div", {"class": "section"})

    # Find sub-sections in each page
    sections = body.findChildren("div", {"class": "section"})

    # Split each page into its major sub-headings.
    split_body = [item for item in sections if len(item.findAll("h2")) != 0]

    return header, url, split_body


def _scraper(url):
    """
    Scraper function

    :Param url: url to be scraped
    :Return: BeautifulSoup object
    """
    response = requests.get(url)
    assert response.status_code == 200, "url could not be reached"

    soup = BeautifulSoup(response.content, "html.parser")

    return soup


def _decompose(args):
    """
    Remove tags and their content

    :Param args: list of items to be decomposed
    """
    for item in args:
        item.decompose()
