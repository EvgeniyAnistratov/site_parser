import re
from urllib.parse import urljoin
import requests
import time
import tracemalloc

import core.db_manager as mydb


TITLE_PATTERN = r"<title[^<>]*>(.+)<\/title>"
URL_PATTERN = r"href=\"([^\"]+)\""
CONTENT_TYPE_NAME = "Content-Type"
CONTENT_TYPE_VALUE = "text/html"
REQUEST_TIMEOUT = 5  # request timeout seconds


def resource_profile(func):
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        start_world_time = time.time()
        start_cpu_time = time.process_time()
        func(*args, **kwargs)
        end_cpu_time = time.process_time()
        end_world_time = time.time()
        _, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        used_memory = peak_memory / 1024 / 1024  # MB
        used_cpu_time = end_cpu_time - start_cpu_time
        used_wold_time = end_world_time - start_world_time
        print(f"Time and memory usage by '{func.__name__}' function.")
        print(f"Maximum used memory: {used_memory:.3f} MB")
        print(f"CPU Execution time: {used_cpu_time:.3f} seconds.")
        print(f"All Execution time: {used_wold_time:.3f} seconds.")
    return wrapper


def re_search(content: str, pattern: str) -> tuple:
    matches = re.findall(pattern, content, re.MULTILINE)
    return matches


class HtmlParser:
    def __init__(self, connection, base_url: str, depth: int):
        self._connection = connection
        self.base_url = base_url
        self.depth = depth

    @resource_profile
    def run_with_profile(self):
        self.parse(self.base_url, self.depth, parent_id=None)

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
