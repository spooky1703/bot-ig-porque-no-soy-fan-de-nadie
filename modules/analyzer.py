"""
Bot IG - Analyzer Module
Compares following and followers lists to find non-followers.
"""

from typing import Dict, List
from utils.logger import get_logger

logger = get_logger(__name__)


def find_non_followers(
    following: Dict[str, dict], 
    followers: Dict[str, dict]
) -> List[dict]:
    """
    Find users that you follow but don't follow you back.
    
    Args:
        following: Dictionary of users you follow
        followers: Dictionary of users who follow you
        
    Returns:
        List of user dictionaries who don't follow you back
    """
    logger.info("Analyzing following vs followers...")
    
    following_ids = set(following.keys())
    followers_ids = set(followers.keys())
    
    # Users you follow but don't follow you back
    non_follower_ids = following_ids - followers_ids
    
    # Build result list with full user info
    non_followers = []
    for user_id in non_follower_ids:
        user_info = following[user_id]
        non_followers.append(user_info)
    
    # Sort by username for consistent output
    non_followers.sort(key=lambda x: x['username'].lower())
    
    logger.info(f"Found {len(non_followers)} non-followers")
    logger.info(f"Stats: {len(following)} following, {len(followers)} followers")
    
    return non_followers


def find_fans(
    following: Dict[str, dict], 
    followers: Dict[str, dict]
) -> List[dict]:
    """
    Find users that follow you but you don't follow back.
    (Bonus function for future use)
    
    Args:
        following: Dictionary of users you follow
        followers: Dictionary of users who follow you
        
    Returns:
        List of user dictionaries who follow you but you don't follow back
    """
    following_ids = set(following.keys())
    followers_ids = set(followers.keys())
    
    fan_ids = followers_ids - following_ids
    
    fans = []
    for user_id in fan_ids:
        user_info = followers[user_id]
        fans.append(user_info)
    
    fans.sort(key=lambda x: x['username'].lower())
    
    logger.info(f"Found {len(fans)} fans (followers you don't follow back)")
    
    return fans


def find_mutual(
    following: Dict[str, dict], 
    followers: Dict[str, dict]
) -> List[dict]:
    """
    Find users that you follow and follow you back (mutual).
    (Bonus function for future use)
    
    Args:
        following: Dictionary of users you follow
        followers: Dictionary of users who follow you
        
    Returns:
        List of user dictionaries with mutual follows
    """
    following_ids = set(following.keys())
    followers_ids = set(followers.keys())
    
    mutual_ids = following_ids & followers_ids
    
    mutuals = []
    for user_id in mutual_ids:
        user_info = following[user_id]
        mutuals.append(user_info)
    
    mutuals.sort(key=lambda x: x['username'].lower())
    
    logger.info(f"Found {len(mutuals)} mutual follows")
    
    return mutuals
