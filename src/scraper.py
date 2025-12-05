# from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import random

def init_driver(headless=True):
    """Initialize Chrome driver with options to avoid detection."""
    options = uc.ChromeOptions()
    if headless:
        options.add_argument("--headless=new") # Use new headless mode for better evasion
        options.add_argument("--window-size=1920,1080") # Set realistic window size
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver = uc.Chrome(options=options, version_main=142)
    return driver

def build_url(zone, price_max=None, listing_type='sale', neighborhood=None):
    """Build Idealista URL based on zone and filters."""
    type_path = "venta-viviendas" if listing_type == 'sale' else "alquiler-viviendas"
    base_url = f"https://www.idealista.com/{type_path}/{zone}/"
    if neighborhood:
        base_url += f"{neighborhood}/"
    if price_max:
        base_url += f"con-precio-hasta_{price_max}/"
    return base_url

def scrape_page(driver, url):
    """Navigate to URL and return HTML content."""
    driver.get(url)
    # Wait for listings to load (adjust selector based on actual site)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "article"))
        )
    except Exception as e:
        print(f"[-] Wait timed out or error: {e}")
        screenshot_path = "debug_screenshot.png"
        driver.save_screenshot(screenshot_path)
        print(f"[-] Saved screenshot to {screenshot_path}")
    
    # Random sleep to mimic human behavior
    time.sleep(random.uniform(2, 5))
    
    return driver.page_source

def parse_listings(html):
    """Parse HTML and extract listings."""
    soup = BeautifulSoup(html, 'html.parser')
    listings = []
    
    # Adjust selectors based on Idealista's actual DOM structure
    articles = soup.find_all('article', class_='item')
    
    for article in articles:
        try:
            listing_id = article.get('data-element-id')
            if not listing_id:
                continue
                
            title_elem = article.find('a', class_='item-link')
            raw_title = title_elem.text.strip() if title_elem else "No Title"
            
            # Start with defaults
            title = raw_title
            location = "N/A"
            
            # In Idealista, the title is usually "Type en Location" (e.g. "Alquiler de piso en Calle Mayor")
            # We split it to separate Type (Title) and Location
            if " en " in raw_title:
               parts = raw_title.split(" en ", 1)
               title = parts[0].strip()
               location = parts[1].strip()
            
            link = "https://www.idealista.com" + title_elem['href'] if title_elem else ""
            
            price_elem = article.find('span', class_='item-price')
            price = price_elem.text.strip() if price_elem else "No Price"
            
            # Extract Square Meters
            sq_meters = "N/A"
            details = article.find_all('span', class_='item-detail')
            for detail in details:
                text = detail.text.strip()
                if 'm²' in text:
                    sq_meters = text
                    break
            
            listings.append({
                'id': listing_id,
                'title': title,
                'price': price,
                'sq_meters': sq_meters,
                'location': location,
                'link': link
            })
        except Exception as e:
            print(f"Error parsing article: {e}")
            continue
            
    return listings
