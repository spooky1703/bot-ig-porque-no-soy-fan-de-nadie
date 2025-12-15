#!/usr/bin/env python3
"""
Bot IG - Instagram Non-Followers Detector
==========================================

This bot identifies Instagram accounts that you follow but don't follow you back.

Usage:
    1. Copy .env.example to .env and fill in your credentials
    2. Install dependencies: pip install -r requirements.txt
    3. Run: python main.py

Author: Bot IG
"""

import sys
from modules.auth import InstagramAuth
from modules.scraper import InstagramScraper
from modules.analyzer import find_non_followers
from modules.exporter import export_all
from utils.logger import get_logger

logger = get_logger(__name__)


def print_banner():
    """Print the application banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   📱 Instagram Non-Followers Detector                     ║
    ║   ─────────────────────────────────────                   ║
    ║   Find accounts that don't follow you back                ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Main entry point for the bot."""
    print_banner()
    
    # Step 1: Authentication
    logger.info("Starting authentication...")
    auth = InstagramAuth()
    
    if not auth.login():
        logger.error("Authentication failed. Please check your credentials.")
        sys.exit(1)
    
    try:
        # Step 2: Scrape data
        logger.info("Starting data collection...")
        scraper = InstagramScraper(auth.get_client(), auth.user_id)
        following, followers = scraper.get_all_data()
        
        if not following:
            logger.warning("Could not fetch following list")
            sys.exit(1)
        
        if not followers:
            logger.warning("Could not fetch followers list")
            sys.exit(1)
        
        # Step 3: Analyze
        logger.info("Analyzing data...")
        non_followers = find_non_followers(following, followers)
        
        # Step 4: Export results
        logger.info("Exporting results...")
        files = export_all(
            non_followers,
            following_count=len(following),
            followers_count=len(followers)
        )
        
        # Summary
        print("\n📁 Files generated:")
        print(f"   • TXT: {files['txt']}")
        print(f"   • JSON: {files['json']}")
        print("\n✅ Analysis complete!")
        
    except KeyboardInterrupt:
        logger.info("\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
