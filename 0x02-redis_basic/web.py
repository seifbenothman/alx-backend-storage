#!/usr/bin/env python3
""" web.py """
import requests
import redis
from functools import wraps
import time

redis_conn = redis.Redis(host='localhost', port=6379, db=0)

def track_and_cache(func):
    """Decorator to track and cache web page content."""
    @wraps(func)
    def wrapper(url):
        """Wrapper function for tracking and caching."""
        url_count_key = f"count:{url}"
        redis_conn.incr(url_count_key)

        cached_content = redis_conn.get(url)
        if cached_content:
            print("Cache hit!")
            return cached_content.decode('utf-8')

        print("Cache miss!")
        response = requests.get(url)
        page_content = response.text

        redis_conn.setex(url, 10, page_content)

        return page_content

    return wrapper

@track_and_cache
def get_page(url: str) -> str:
    """Fetch the page content of a URL."""
    return requests.get(url).text

if __name__ == "__main__":
    url = ("http://slowwly.robertomurray.co.uk/"
           "delay/1000/url/"
           "https://www.example.com")
    print(get_page(url))
    print(get_page(url))
    print(get_page(url))

    time.sleep(11)
    print(get_page(url))

    access_count = redis_conn.get(f"count:{url}")
    if access_count:
        print(f"URL was accessed {access_count.decode('utf-8')} times.")
    else:
        print("URL access count not found.")
