import re

import requests

from bs4 import BeautifulSoup

BASE_URL = 'https://docs.python.org/3/reference/'


def main():
    """
    Scrape base url and extract links

    :Return: parsed content
    """
    content = _scraper(BASE_URL)
    links = content.findAll(href=_has_no_hashtag)

    # We want to get only the 10 chapters of the reference
    start = 17
    end = -14
    links = links[start:end]

    result = _handle_links(links)
    return list(result)


def _has_no_hashtag(href):
    """
    Remove sub chapters

    :Param href: tags with the `href` attribute
    :Return: True if `href` exists and does not contain a hashtag
             else return False
    """
    return href and not re.compile("#").search(href)


def _handle_links(links):
    """
    Scrape and parse links

    :Param links: links to be parsed
    :Return: tuple of (header, url, body)
    """
    for link in links:
        url = f"{BASE_URL}{link.get('href')}"
        content = _scraper(url)

        permalink = content.findChildren("a", {"class": "headerlink"})
        _decompose(permalink)

        header = content.find('h1').text.lstrip('0123456789. ')
        body = content.find("div", {"class": "document"})

        sphinxsidebar = body.findChild("div", {"class": "sphinxsidebar"})
        _decompose([sphinxsidebar])

        yield header, url, body


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
