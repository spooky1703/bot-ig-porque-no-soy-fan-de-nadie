"""
Bot IG - Authentication Module
Handles Instagram login and session management.
"""

from pathlib import Path
from instagrapi import Client
from instagrapi.exceptions import (
    LoginRequired,
    TwoFactorRequired,
    ChallengeRequired,
    BadPassword,
    UserNotFound,
    ClientError,
)
from config import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, SESSION_FILE
from utils.logger import get_logger

logger = get_logger(__name__)


class InstagramAuth:
    """
    Handles Instagram authentication with session persistence.
    """
    
    def __init__(self):
        """Initialize the authentication handler."""
        self.client = Client()
        self.user_id = None
        self._configure_client()
    
    def _configure_client(self):
        """Configure client settings to avoid detection."""
        # Set device settings to appear as a real Android device
        self.client.set_device({
            "app_version": "269.0.0.18.75",
            "android_version": 26,
            "android_release": "8.0.0",
            "dpi": "480dpi",
            "resolution": "1080x1920",
            "manufacturer": "OnePlus",
            "device": "devitron",
            "model": "6T Dev",
            "cpu": "qcom",
            "version_code": "314665256",
        })
        # Set delays between requests
        self.client.delay_range = [1, 3]
    
    def _load_session(self) -> bool:
        """
        Try to load an existing session from file.
        
        Returns:
            True if session was loaded successfully, False otherwise
        """
        session_path = Path(SESSION_FILE)
        if not session_path.exists():
            logger.debug("No session file found")
            return False
        
        try:
            self.client.load_settings(session_path)
            self.client.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
            self.user_id = self.client.user_id
            logger.info("Session loaded successfully")
            return True
        except Exception as e:
            logger.warning(f"Could not load session: {e}")
            session_path.unlink(missing_ok=True)
            return False
    
    def _save_session(self):
        """Save the current session to file."""
        try:
            self.client.dump_settings(Path(SESSION_FILE))
            logger.debug("Session saved")
        except Exception as e:
            logger.warning(f"Could not save session: {e}")
    
    def login(self) -> bool:
        """
        Login to Instagram.
        
        First attempts to use an existing session, then falls back to
        username/password login.
        
        Returns:
            True if login was successful, False otherwise
        """
        if not INSTAGRAM_USERNAME or not INSTAGRAM_PASSWORD:
            logger.error("Instagram credentials not configured!")
            logger.error("Please copy .env.example to .env and fill in your credentials")
            return False
        
        # Try loading existing session first
        if self._load_session():
            return True
        
        # Fresh login
        logger.info(f"Logging in as {INSTAGRAM_USERNAME}...")
        
        try:
            self.client.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
            self.user_id = self.client.user_id
            self._save_session()
            logger.info("Login successful!")
            return True
            
        except BadPassword:
            logger.error("Invalid password")
            return False
            
        except UserNotFound:
            logger.error("Invalid username")
            return False
            
        except TwoFactorRequired:
            logger.warning("Two-factor authentication required")
            return self._handle_2fa()
            
        except ChallengeRequired:
            logger.error("Instagram challenge required (suspicious login detected)")
            logger.error("Please login manually in the app to verify your identity")
            return False
            
        except LoginRequired:
            logger.error("Login required - session may have expired")
            return False
            
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return False
    
    def _handle_2fa(self) -> bool:
        """
        Handle two-factor authentication.
        
        Returns:
            True if 2FA was successful, False otherwise
        """
        try:
            code = input("Enter 2FA code: ").strip()
            self.client.two_factor_login(code)
            self.user_id = self.client.user_id
            self._save_session()
            logger.info("2FA login successful!")
            return True
        except Exception as e:
            logger.error(f"2FA failed: {e}")
            return False
    
    def logout(self):
        """Logout from Instagram."""
        try:
            self.client.logout()
            logger.info("Logged out successfully")
        except Exception as e:
            logger.warning(f"Logout error: {e}")
    
    def is_authenticated(self) -> bool:
        """
        Check if the client is authenticated.
        
        Returns:
            True if authenticated, False otherwise
        """
        return self.user_id is not None
    
    def get_client(self) -> Client:
        """
        Get the authenticated client instance.
        
        Returns:
            The instagrapi Client instance
        """
        return self.client
