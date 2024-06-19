import requests
import time
import sys
import logging
from typing import Optional
from functools import wraps

logging.basicConfig(level=logging.INFO)


def retry(exceptions, tries: int = 3, delay: int = 5, backoff: int = 2) -> callable:
    """
    Retry decorator to retry a function on specific exceptions.

    Args:
    - exceptions (tuple): Tuple of exceptions to retry on.
    - tries (int): Number of retry attempts.
    - delay (int): Initial delay between retries in seconds.
    - backoff (int): Backoff multiplier for delay.

    Returns:
    - callable: Decorator function.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    logging.error(f'{func.__name__} {e}, Retrying in {mdelay} seconds...')
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return func(*args, **kwargs)

        return wrapper

    return decorator


@retry((requests.exceptions.RequestException,), tries=3, delay=5, backoff=2)
def ping_website(url: str) -> None:
    """
    Ping a website repeatedly until successful or retries are exhausted.

    Args:
    - url (str): The URL of the website to ping.

    Returns:
    - None
    """
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for non-200 status codes
    logging.info("Website is up!")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ping_util.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    ping_website(url)
