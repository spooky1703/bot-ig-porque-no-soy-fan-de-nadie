"""
Bot IG - Scraper Module
Obtains following and followers lists from Instagram.
"""

from typing import Dict, List
from instagrapi import Client
from utils.logger import get_logger
from utils.rate_limiter import rate_limiter

logger = get_logger(__name__)


class InstagramScraper:
    """
    Scrapes following and followers data from Instagram.
    """
    
    def __init__(self, client: Client, user_id: str):
        """
        Initialize the scraper.
        
        Args:
            client: Authenticated instagrapi Client
            user_id: The user ID to scrape data for
        """
        self.client = client
        self.user_id = user_id
    
    def get_following(self) -> Dict[str, dict]:
        """
        Get the list of users that you follow.
        
        Returns:
            Dictionary mapping user_id to user info
        """
        logger.info("Fetching following list...")
        
        try:
            following = self.client.user_following(self.user_id)
            logger.info(f"Found {len(following)} following")
            
            # Convert to simplified format
            result = {}
            for user_id, user_info in following.items():
                result[str(user_id)] = {
                    'user_id': str(user_id),
                    'username': user_info.username,
                    'full_name': getattr(user_info, 'full_name', '') or '',
                    'is_private': getattr(user_info, 'is_private', False),
                    'is_verified': getattr(user_info, 'is_verified', False),
                }
            
            rate_limiter.wait_long(reason="after fetching following")
            return result
            
        except Exception as e:
            logger.error(f"Error fetching following: {e}")
            return {}
    
    def get_followers(self) -> Dict[str, dict]:
        """
        Get the list of users that follow you.
        
        Returns:
            Dictionary mapping user_id to user info
        """
        logger.info("Fetching followers list...")
        
        try:
            followers = self.client.user_followers(self.user_id)
            logger.info(f"Found {len(followers)} followers")
            
            # Convert to simplified format
            result = {}
            for user_id, user_info in followers.items():
                result[str(user_id)] = {
                    'user_id': str(user_id),
                    'username': user_info.username,
                    'full_name': getattr(user_info, 'full_name', '') or '',
                    'is_private': getattr(user_info, 'is_private', False),
                    'is_verified': getattr(user_info, 'is_verified', False),
                }
            
            rate_limiter.wait_long(reason="after fetching followers")
            return result
            
        except Exception as e:
            logger.error(f"Error fetching followers: {e}")
            return {}
    
    def get_all_data(self) -> tuple:
        """
        Get both following and followers lists.
        
        Returns:
            Tuple of (following_dict, followers_dict)
        """
        following = self.get_following()
        rate_limiter.wait(reason="between API calls")
        followers = self.get_followers()
        
        return following, followers
