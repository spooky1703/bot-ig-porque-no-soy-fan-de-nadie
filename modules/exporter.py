"""
Bot IG - Exporter Module
Exports analysis results to various formats.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List
from config import OUTPUT_DIR
from utils.logger import get_logger

logger = get_logger(__name__)


def _get_timestamp() -> str:
    """Get current timestamp for filenames."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def export_to_console(non_followers: List[dict], show_details: bool = True):
    """
    Print non-followers to console in a readable format.
    
    Args:
        non_followers: List of non-follower user dictionaries
        show_details: Whether to show full details or just usernames
    """
    print("\n" + "=" * 60)
    print("📊 NON-FOLLOWERS REPORT")
    print("=" * 60)
    print(f"Total non-followers: {len(non_followers)}")
    print("-" * 60)
    
    if not non_followers:
        print("🎉 Everyone you follow follows you back!")
        print("=" * 60 + "\n")
        return
    
    for i, user in enumerate(non_followers, 1):
        username = user['username']
        full_name = user.get('full_name', '')
        verified = "✓" if user.get('is_verified') else ""
        private = "🔒" if user.get('is_private') else ""
        
        if show_details and full_name:
            print(f"{i:3}. @{username} {verified}{private} ({full_name})")
        else:
            print(f"{i:3}. @{username} {verified}{private}")
    
    print("=" * 60 + "\n")


def export_to_txt(non_followers: List[dict], filename: str = None) -> Path:
    """
    Export non-followers to a text file (one username per line).
    
    Args:
        non_followers: List of non-follower user dictionaries
        filename: Optional custom filename
        
    Returns:
        Path to the created file
    """
    if filename is None:
        filename = f"non_followers_{_get_timestamp()}.txt"
    
    filepath = OUTPUT_DIR / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"# Non-Followers Report\n")
        f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Total: {len(non_followers)}\n")
        f.write("#" + "-" * 40 + "\n\n")
        
        for user in non_followers:
            f.write(f"@{user['username']}\n")
    
    logger.info(f"Exported to TXT: {filepath}")
    return filepath


def export_to_json(
    non_followers: List[dict], 
    following_count: int = 0,
    followers_count: int = 0,
    filename: str = None
) -> Path:
    """
    Export non-followers to a JSON file with full details.
    
    Args:
        non_followers: List of non-follower user dictionaries
        following_count: Total number of following
        followers_count: Total number of followers
        filename: Optional custom filename
        
    Returns:
        Path to the created file
    """
    if filename is None:
        filename = f"non_followers_{_get_timestamp()}.json"
    
    filepath = OUTPUT_DIR / filename
    
    report = {
        'generated_at': datetime.now().isoformat(),
        'stats': {
            'non_followers_count': len(non_followers),
            'following_count': following_count,
            'followers_count': followers_count,
        },
        'non_followers': non_followers,
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Exported to JSON: {filepath}")
    return filepath


def export_all(
    non_followers: List[dict],
    following_count: int = 0,
    followers_count: int = 0
) -> dict:
    """
    Export to all formats (console, txt, json).
    
    Args:
        non_followers: List of non-follower user dictionaries
        following_count: Total number of following
        followers_count: Total number of followers
        
    Returns:
        Dictionary with paths to created files
    """
    timestamp = _get_timestamp()
    
    # Console output
    export_to_console(non_followers)
    
    # File exports
    txt_path = export_to_txt(non_followers, f"non_followers_{timestamp}.txt")
    json_path = export_to_json(
        non_followers, 
        following_count, 
        followers_count,
        f"non_followers_{timestamp}.json"
    )
    
    return {
        'txt': txt_path,
        'json': json_path,
    }
