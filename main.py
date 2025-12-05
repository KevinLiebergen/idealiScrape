import asyncio
import sys
import argparse
from src.scraper import init_driver, scrape_page, parse_listings, build_url
from src.database import init_db, listing_exists, save_listing
from src.notifier import send_message
import src.settings as settings

async def main():
    parser = argparse.ArgumentParser(description='Scrape Idealista for real estate listings.')
    parser.add_argument('--zone', type=str, default='madrid', help='Zone to search (e.g., madrid, barcelona)')
    parser.add_argument('--neighborhood', type=str, default='ciudad-lineal', help='Neighborhood to search (e.g., ciudad-lineal)')
    parser.add_argument('--price-max', type=int, default=1000, help='Maximum price filter')
    parser.add_argument('--type', type=str, default='rent', choices=['sale', 'rent'], help='Type of listing: sale or rent')
    parser.add_argument('--no-headless', action='store_true', help='Run with visible browser (not headless)')
    args = parser.parse_args()

    print("[+] Starting Idealista Scraper...")
    
    # 1. Initialize DB
    init_db()
    print("[+] Database initialized.")
    
    # 2. Init Driver
    # Default is invisible (headless=True) unless --no-headless is specified
    driver = init_driver(headless=not args.no_headless)
    print("[+] Driver initialized.")
    
    try:
        # 3. Scrape
        target_url = build_url(args.zone, args.price_max, args.type, args.neighborhood)
        print(f"[+] Scraping {target_url}")
        html = scrape_page(driver, target_url)
        
        # 4. Parse
        listings = parse_listings(html)
        print(f"[+] Found {len(listings)} listings.")
        
        new_listings_count = 0
        for listing in listings:
            if not listing_exists(listing['id']):
                # 5. Save & Notify
                save_listing(listing)
                new_listings_count += 1
                
                msg = f"🏠 *New Listing Found!*\n\n🏷 *Title:* {listing['title']}\n📍 *Location:* {listing.get('location', 'N/A')}\n💰 *Price:* {listing['price']}\n📏 *Size:* {listing.get('sq_meters', 'N/A')}\n🔗 [View Listing]({listing['link']})"
                await send_message(settings.TELEGRAM_TOKEN, settings.TELEGRAM_CHAT_ID, msg)
                
                # Respect Telegram rate limits
                await asyncio.sleep(3)
        
        print(f"[+] Scrape complete. {new_listings_count} new listings found.")
        
    except Exception as e:
        print(f"[+] An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    asyncio.run(main())
