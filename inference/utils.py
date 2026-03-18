import logging
import time
from typing import Callable, Any

logger = logging.getLogger("airline_delay_inference")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)


def log_request(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Any:
        start = time.time()
        try:
            result = func(*args, **kwargs)
            elapsed = (time.time() - start) * 1000
            logger.info(f"{func.__name__} completed in {elapsed:.2f} ms")
            return result
        except Exception as e:
            elapsed = (time.time() - start) * 1000
            logger.exception(
                f"Error in {func.__name__} after {elapsed:.2f} ms: {e}"
            )
            raise
    return wrapper
