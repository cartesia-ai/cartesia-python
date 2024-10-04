import asyncio
import time
from functools import wraps
from http.client import RemoteDisconnected

from aiohttp.client_exceptions import ServerDisconnectedError
from httpx import TimeoutException
from requests.exceptions import ConnectionError


def retry_on_connection_error(max_retries=3, backoff_factor=1, logger=None):
    """Retry a function if a ConnectionError, RemoteDisconnected, ServerDisconnectedError, or TimeoutException occurs.

    Args:
        max_retries (int): The maximum number of retries.
        backoff_factor (int): The factor to increase the delay between retries.
        logger (logging.Logger): The logger to use for logging.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retry_count = 0
            while retry_count < max_retries:
                try:
                    return func(*args, **kwargs)
                except (
                    ConnectionError,
                    RemoteDisconnected,
                    ServerDisconnectedError,
                    TimeoutException,
                ) as e:
                    logger.info(f"Retrying after exception: {e}")
                    retry_count += 1
                    if retry_count < max_retries:
                        delay = backoff_factor * (2 ** (retry_count - 1))
                        logger.warn(
                            f"Attempt {retry_count + 1}/{max_retries} in {delay} seconds..."
                        )
                        time.sleep(delay)
                    else:
                        raise Exception(f"Exception occurred after {max_retries} tries.") from e

        return wrapper

    return decorator


def retry_on_connection_error_async(max_retries=3, backoff_factor=1, logger=None):
    """Retry an asynchronous function if a ConnectionError, RemoteDisconnected, ServerDisconnectedError, or TimeoutException occurs.

    Args:
        max_retries (int): The maximum number of retries.
        backoff_factor (int): The factor to increase the delay between retries.
        logger (logging.Logger): The logger to use for logging.
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            retry_count = 0
            while retry_count < max_retries:
                try:
                    async for chunk in func(*args, **kwargs):
                        yield chunk
                    # If the function completes without raising an exception return
                    return
                except (
                    ConnectionError,
                    RemoteDisconnected,
                    ServerDisconnectedError,
                    TimeoutException,
                ) as e:
                    logger.info(f"Retrying after exception: {e}")
                    retry_count += 1
                    if retry_count < max_retries:
                        delay = backoff_factor * (2 ** (retry_count - 1))
                        logger.warn(
                            f"Attempt {retry_count + 1}/{max_retries} in {delay} seconds..."
                        )
                        await asyncio.sleep(delay)
                    else:
                        raise Exception(f"Exception occurred after {max_retries} tries.") from e

        return wrapper

    return decorator
