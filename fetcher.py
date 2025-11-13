import requests
from bs4 import BeautifulSoup

README_URL = "https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/dev/README.md"

def fetch_readme():
    resp = requests.get(README_URL)
    resp.raise_for_status()
    return resp.text

def extract_listings(md_content, max_age_days=2):
    """
    Returns a list of dicts for internships <= max_age_days:
    [
        {
            "company": str,
            "role": str,
            "location": str,
            "link": str,
            "age": str
        },
        ...
    ]
    """
    soup = BeautifulSoup(md_content, "html.parser")
    listings = []

    table = soup.find("table")
    if not table:
        return listings

    rows = table.find_all("tr")[1:] 
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 5:
            continue

        company = cols[0].get_text(strip=True)
        role = cols[1].get_text(strip=True)
        
        location_tag = cols[2]
        location = location_tag.get_text(separator=", ", strip=True)
        
        app_links = cols[3].find_all("a")
        link = app_links[0]['href'] if app_links else ""
        
        age_text = cols[4].get_text(strip=True)
      
        try:
            age_days = int(age_text.rstrip('d'))
        except ValueError:
            age_days = max_age_days + 1 
        
        if age_days > max_age_days:
            continue 
        
        listings.append({
            "company": company,
            "role": role,
            "location": location,
            "link": link,
            "age": age_text
        })

    return listings
