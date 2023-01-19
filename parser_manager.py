import re
from urllib.parse import urljoin
import requests

import db_manager as mydb


TITLE_PATTERN = r"<title[^<>]*>(.+)<\/title>"
URL_PATTERN = r"href=\"([^\"]+)\""
CONTENT_TYPE_NAME = "Content-Type"
CONTENT_TYPE_VALUE = "text/html"
REQUEST_TIMEOUT = 5  # request timeout seconds


def re_search(content: str, pattern: str) -> tuple:
    matches = re.findall(pattern, content, re.MULTILINE)
    return matches


class HtmlParser:
    def __init__(self, connection):
        self._connection = connection

    def parse(self, base_url: str, depth: int, parent_id: int = None):
        """
        Gets an html page from url, saves the page data to a database, and
        sends requests recursively to all the urls on the page if depth != 0.
        """
        try:
            response = requests.get(base_url, timeout=REQUEST_TIMEOUT)
        # Ignore incorrect url
        except requests.exceptions.MissingSchema:
            return
        except requests.exceptions.InvalidSchema:
            return
        except requests.exceptions.ConnectionError:
            return

        content_type = response.headers.get(CONTENT_TYPE_NAME)

        if response.status_code == 200 and content_type and \
                CONTENT_TYPE_VALUE in content_type:
            title = re_search(response.text, TITLE_PATTERN)
            title = title[0] if title else None
            data = [(parent_id, response.text, title, base_url), ]
            row_id = mydb.insert_to_db(self._connection, data)
            if depth != 0:
                urls = re_search(response.text, URL_PATTERN)
                del response
                for url in urls:
                    absolute_url = urljoin(base_url, url)
                    self.parse(absolute_url, depth-1, row_id)
