#!/usr/bin/env python3
""" Module for web functions """

import requests
import redis
from functools import wraps


def track_and_cache(func):
    """ Decorator to track and cache page requests """
    @wraps(func)
    def wrapper(url):
        """ Wrapper function to track and cache page requests """
        redis_conn = redis.Redis()

        url_count_key = f"count:{url}"
        redis_conn.incr(url_count_key)

        cached_content = redis_conn.get(url)
        if cached_content:
            return cached_content.decode('utf-8')

        response = requests.get(url)
        page_content = response.text

        redis_conn.setex(url, 10, page_content)

        return page_content

    return wrapper


@track_and_cache
def get_page(url: str) -> str:
    """ Function to get page content """
    return requests.get(url).text


if __name__ == "__main__":
    url = ("http://slowwly.robertomurray.co.uk/"
           "delay/1000/url/"
           "https://www.example.com")
    print(get_page(url))