import requests
from typing import Optional, Tuple
from .logger import logger

def get_coordinates(zone_name: str) -> Optional[Tuple[str, str]]:
    """
    Resolve a zone name to coordinates (lat, lon) using OpenStreetMap Nominatim API.
    
    Args:
        zone_name (str): The name of the zone/city to search for.
        
    Returns:
        Optional[Tuple[str, str]]: A tuple of (latitude, longitude) strings, or None if not found.
    """
    url = "https://nominatim.openstreetmap.org/search"
    
    # Nominatim requires a User-Agent identify your application
    headers = {
        "User-Agent": "IdealiScrape/1.0"
    }
    
    params = {
        "q": zone_name,
        "format": "json",
        "limit": 1
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if not data:
            return None
            
        # Nominatim returns lat/lon as strings
        lat = data[0].get("lat")
        lon = data[0].get("lon")
        
        if lat and lon:
            return lat, lon
            
    except requests.RequestException as e:
        logger.error(f"[-] Geocoding Error: {e}")
        return None
        
    return None
