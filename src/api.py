import requests
import base64
import time
from .logger import logger

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
        
        # Encoding credentials as per Idealista (and standard OAuth Client Credentials)
        # Often it requires base64(key:secret) in Authorization header
        credentials = f"{self.api_key}:{self.api_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {"grant_type": "client_credentials"}
        
        try:
            response = requests.post(url, headers=headers, data=data, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            self.token = result.get("access_token")
            # Set expiry (usually lasts 1 hour, subtract buffer)
            expires_in = result.get("expires_in", 3600)
            self.token_expiry = time.time() + expires_in - 60
            
            logger.info("[+] API Token retrieved successfully.")
            return self.token
            
        except requests.exceptions.RequestException as e:
            logger.error(f"[-] Failed to get API Token: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"[-] Response Content: {e.response.text}")
            raise

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
            "Content-Type": "application/x-www-form-urlencoded"
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

        # The API usually takes POST for complex searches or GET with query params.
        # Standard documentation usually expects POST with form-data or GET.
        # Let's assume POST for /search based on typical usage, or try GET if documented otherwise.
        # Actually most examples show POST.
        
        try:
            response = requests.post(url, headers=headers, data=params, timeout=15)
            response.raise_for_status()
            return response.json()  # Returns list of elements usually
        except requests.exceptions.RequestException as e:
            logger.error(f"[-] Search Request Failed: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"[-] Response Content: {e.response.text}")
            return []
