#!/usr/bin/env python3
""" web.py """
import requests
import redis
from functools import wraps

# Initialize Redis connection
redis_conn = redis.Redis()

def track_and_cache(func):
    """Decorator to track and cache web page content."""
    @wraps(func)
    def wrapper(url):
        """Wrapper function for tracking and caching."""
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
    """Fetch the page content of a URL."""
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    url = ("http://slowwly.robertomurray.co.uk/"
           "delay/1000/url/"
           "https://www.example.com")
    print(get_page(url))  # First call, should fetch from the web
    print(get_page(url))  # Second call within 10 seconds, should fetch from cache
    print(get_page(url))  # Third call within 10 seconds, should fetch from cache

    import time
    time.sleep(11)  # Wait for the cache to expire
    print(get_page(url))  # Fourth call after cache expiration, should fetch from the web again
