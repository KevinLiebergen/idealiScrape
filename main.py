import asyncio
import argparse
import sys
from src.settings import (
    TELEGRAM_TOKEN, 
    TELEGRAM_CHAT_ID, 
    IDEALISTA_API_KEY, 
    IDEALISTA_API_SECRET
)
from src.database import init_db, save_listing, listing_exists
from src.notifier import send_message
from src.api import IdealistaAPI

from src.geocoder import get_coordinates

# Default center (Madrid Sol)
DEFAULT_CENTER = "40.4167,-3.70325" 

async def main():
    parser = argparse.ArgumentParser(description="Idealista API Scraper")
    
    # Mutually exclusive group for location: either center or zone
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--center", type=str, help="Center of search (lat,lng), e.g. '40.4167,-3.70325'")
    group.add_argument("--zone", type=str, help="Name of zone/city to search (e.g. 'Madrid', 'Barcelona')")
    
    parser.add_argument("--distance", type=int, default=3000, help="Distance in meters from center")
    parser.add_argument("--price-max", type=int, default=1000, help="Max price")
    parser.add_argument("--type", type=str, default="rent", choices=['sale', 'rent'], help="Listing type")
    
    args = parser.parse_args()

    # Determine center
    center = DEFAULT_CENTER
    
    if args.center:
        center = args.center
    elif args.zone:
        print(f"[*] Resolving coordinates for zone: '{args.zone}'...")
        coords = get_coordinates(args.zone)
        if coords:
            center = f"{coords[0]},{coords[1]}"
            print(f"[+] Coordinates found: {center}")
        else:
            print(f"[-] Could not resolve coordinates for '{args.zone}'. Using default center.")
    else:
        # Neither specified, stick to default
        pass

    # 1. Init DB
    init_db()
    print("[+] Database initialized.")

    # 2. Init API
    if not IDEALISTA_API_KEY or not IDEALISTA_API_SECRET:
        print("[-] Error: API credentials missing. Check .env")
        sys.exit(1)
        
    api = IdealistaAPI(IDEALISTA_API_KEY, IDEALISTA_API_SECRET)

    # 3. Search
    print(f"[+] Searching via API | Type: {args.type} | Center: {center} | Max Price: {args.price_max}")
    
    try:
        results = api.search_properties(
            center=center,
            distance=args.distance,
            operation=args.type,
            maxPrice=args.price_max,
            minSize=None # Can add more args later
        )
    except Exception as e:
        print(f"[-] API Error: {e}")
        return

    listings = results.get("elementList", [])
    print(f"[+] Found {len(listings)} listings.")

    new_count = 0
    
    for item in listings:
        # Map API response to our DB schema
        # API fields: propertyCode, price, size, rooms, address, url, thumbnail, etc.
        listing_id = str(item.get("propertyCode"))
        
        if not listing_id:
            continue
            
        if listing_exists(listing_id):
            continue

        # Extract details
        title = item.get("suggestedTexts", {}).get("title", item.get("address", "No Title"))
        price = f"{item.get('price'):,} {item.get('currencySuffix', '€')}"
        link = item.get("url")
        sq_meters = f"{item.get('size')} m²"
        address = item.get("address", "Unknown Location")
        neighborhood = item.get("neighborhood")
        district = item.get("district")
        
        location = address
        extra_info = []
        if neighborhood:
            extra_info.append(neighborhood)
        if district:
            extra_info.append(district)
            
        if extra_info:
            location += f" ({', '.join(extra_info)})"
        
        # Save to DB
        save_listing({
            "id": listing_id,
            "title": title,
            "price": price,
            "link": link,
            "sq_meters": sq_meters,
            "location": location
        })
        new_count += 1
        
        # Notify
        # Format: 🏠 Title \n 📍 Location \n 💰 Price \n 📏 Size \n 🔗 Link
        msg = f"🏠 *{title}*\n📍 {location}\n💰 {price}\n📏 {sq_meters}\n🔗 [View on Idealista]({link})"
        
        await send_message(TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, msg)
        
        # Slight delay to respect Telegram limits
        await asyncio.sleep(3)

    print(f"[+] Process complete. {new_count} new listings saved and notified.")

if __name__ == "__main__":
    asyncio.run(main())
