from db import init_db, get_existing_listings, insert_new_listings, clear_listings
from fetcher import fetch_readme, extract_listings
from mailer import send_email

def run():
    print("🔍 Checking for new internships...")
    init_db()
    
    md_content = fetch_readme()
    listings = extract_listings(md_content)
    
    existing = get_existing_listings()
    
    new = [l for l in listings if l['link'] not in {e['link'] for e in existing}]
    
    if new:
        print(f"🆕 Found {len(new)} new listings.")
        insert_new_listings(new)
        send_email(new, name="Anthony")
    else:
        print("No new recent listings found.")

if __name__ == "__main__":
    run()
