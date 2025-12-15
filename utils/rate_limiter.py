"""
Bot IG - Rate Limiter Utility
Controls timing between API requests to avoid detection.
"""

import random
import time
from config import MIN_DELAY, MAX_DELAY
from utils.logger import get_logger

logger = get_logger(__name__)


class RateLimiter:
    """
    Rate limiter with random delays to avoid bot detection.
    """
    
    def __init__(self, min_delay: float = None, max_delay: float = None):
        """
        Initialize the rate limiter.
        
        Args:
            min_delay: Minimum delay in seconds (default from config)
            max_delay: Maximum delay in seconds (default from config)
        """
        self.min_delay = min_delay or MIN_DELAY
        self.max_delay = max_delay or MAX_DELAY
        self.last_request_time = 0
    
    def wait(self, reason: str = "rate limit"):
        """
        Wait for a random amount of time between requests.
        
        Args:
            reason: Description of why we're waiting (for logging)
        """
        delay = random.uniform(self.min_delay, self.max_delay)
        logger.debug(f"Waiting {delay:.2f}s ({reason})")
        time.sleep(delay)
        self.last_request_time = time.time()
    
    def wait_long(self, multiplier: float = 3.0, reason: str = "extended pause"):
        """
        Wait for a longer period (useful after large operations).
        
        Args:
            multiplier: How much longer than normal delay
            reason: Description of why we're waiting
        """
        delay = random.uniform(self.min_delay * multiplier, self.max_delay * multiplier)
        logger.info(f"Extended wait: {delay:.2f}s ({reason})")
        time.sleep(delay)
        self.last_request_time = time.time()


# Global rate limiter instance
rate_limiter = RateLimiter()
