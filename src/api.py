import requests
import base64
import time
import subprocess
import json

try:
    from .logger import logger
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

from urllib.parse import quote

class IdealistaAuthError(Exception):
    """Custom exception for Idealista Authentication errors."""
    pass

class IdealistaSearchError(Exception):
    """Custom exception for Idealista Search errors."""
    pass

class IdealistaAPI:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.token = None
        self.token_expiry = 0
        self.base_url = "https://api.idealista.com/3.5"

    def _get_token(self):
        """Retrieve OAuth2 Bearer token."""
        # Return existing valid token
        if self.token and time.time() < self.token_expiry:
            return self.token

        url = "https://api.idealista.com/oauth/token"
        
        # User specified RFC 1738 encoding.
        credentials = f"{quote(self.api_key, safe='')}:{quote(self.api_secret, safe='')}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        # Fallback to system Curl as requested due to persistent behaviors with Python Requests
        command = [
            "curl", 
            "-X", "POST",
            "-H", f"Authorization: Basic {encoded_credentials}",
            "-H", "Content-Type: application/x-www-form-urlencoded",
            "-d", "grant_type=client_credentials&scope=read",
            url,
            "-k", # Insecure/Skip SSL as requested
            "-s"  # Silent mode to avoid progress bar in output
        ]
        
        try:
            logger.info("[*] Executing curl for token...")
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            
            # Curl output is expected to be the JSON response
            response_json = json.loads(result.stdout)
            
            self.token = response_json.get("access_token")
            # Set expiry (usually lasts 1 hour, subtract buffer)
            expires_in = response_json.get("expires_in", 3600)
            self.token_expiry = time.time() + expires_in - 60
            
            logger.info("[+] API Token retrieved successfully via curl.")
            return self.token
            
        except subprocess.CalledProcessError as e:
            error_msg = f"[-] Curl command failed: {e}\nStderr: {e.stderr}"
            logger.error(error_msg)
            raise IdealistaAuthError(error_msg) from e
        except json.JSONDecodeError as e:
            error_msg = f"[-] Failed to decode JSON from curl output: {e}\nOutput: {result.stdout}"
            logger.error(error_msg)
            raise IdealistaAuthError(error_msg) from e

    def search_properties(self, center=None, country="es", max_items=20, **kwargs):
        """
        Search for properties.
        Args:
            center (str): Lat,Lng (e.g., '40.4167,-3.70325')
            country (str): 'es', 'it', 'pt'
            max_items (int): Pagination limit
            **kwargs: Additional filters (operation, propertyType, minPrice, maxPrice, etc.)
        """
        token = self._get_token()
        url = f"{self.base_url}/{country}/search"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "curl/7.81.0",
            "Accept": "*/*"
        }
        
        # Default params
        params = {
            "center": center, 
            "maxItems": max_items,
            "numPage": 1,
            "operation": kwargs.get("operation", "sale"),
            "propertyType": kwargs.get("propertyType", "homes"),
            # Idealista API usually requires specific parameters like 'distance' when 'center' is used
            "distance": kwargs.get("distance", 3000), # Default 3km
            "sort": "desc"
        }
        
        # Update with dynamic kwargs (overriding defaults if provided)
        # Filter out None values
        params.update({k: v for k, v in kwargs.items() if v is not None})

        # Update with dynamic kwargs (overriding defaults if provided)
        # Filter out None values
        params.update({k: v for k, v in kwargs.items() if v is not None})

        # Fallback to system Curl as requested due to persistent behaviors with Python Requests
        try:
            from urllib.parse import urlencode
            data_str = urlencode(params)
            
            command = [
                "curl", 
                "-X", "POST",
                "-H", f"Authorization: Bearer {token}",
                "-H", "Content-Type: application/x-www-form-urlencoded",
                "-d", data_str,
                url,
                "-k", # Insecure/Skip SSL as requested
                "-s"  # Silent mode
            ]
            
            logger.info("[*] Executing curl for search...")
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            
            # Curl output is expected to be the JSON response
            return json.loads(result.stdout)

        except subprocess.CalledProcessError as e:
            error_msg = f"[-] Curl search command failed: {e}\nStderr: {e.stderr}"
            logger.error(error_msg)
            raise IdealistaSearchError(error_msg) from e
        except json.JSONDecodeError as e:
            error_msg = f"[-] Failed to decode JSON from curl search output: {e}\nOutput: {result.stdout}"
            logger.error(error_msg)
            # If empty output, return empty dict as originally intended, or raise error?
            # Sticking to raising error to notify user via Telegram as per previous instruction
            raise IdealistaSearchError(error_msg) from e
