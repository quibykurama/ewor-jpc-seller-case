import requests
from bs4 import BeautifulSoup
import json

# List of all URLs to scrape
start_urls = [
    "https://www.ewor.com",
    "https://www.ewor.com/ideation-fellowship",
    "https://www.ewor.com/traction-fellowship",
    "https://www.ewor.com/founder-resources",
    "https://www.ewor.com/startup-templates",
    "https://www.ewor.com/ewor-team",
    "https://form.ewor.com",
    "https://platform.ewor.com",
    "https://www.ewor.com/apply",
    "https://docs.google.com/document/d/1Y2Y3Z4A5B6C7D8E9F0G1H2I3J4K5L6M7N8O9P0Q1R2S",
    "https://reminder.ewor.com",
    "https://www.ewor.com/leaderboard",
    "https://www.ewor.com/legal/imprint",
    "https://www.ewor.com/privacy-policy",
    "https://www.ewor.com/terms-conditions",
    "https://www.ewor.com/blog",
    "https://www.ewor.com/faq",
]

# Set to store visited URLs
visited = set()

# List to store the scraped data
scraped_data = []

def scrape_page(url):
    """Scrape a single page and extract relevant data."""
    if url in visited:
        return
    visited.add(url)
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract data
        title = soup.title.string.strip() if soup.title else "No title"
        meta_description = soup.find("meta", {"name": "description"})
        meta_description = meta_description["content"].strip() if meta_description else "No description"
        content = " ".join([p.get_text(strip=True) for p in soup.find_all("p")])

        # Save the data
        scraped_data.append({
            "url": url,
            "title": title,
            "meta_description": meta_description,
            "content": content,
        })

        # Find and follow internal links
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if href.startswith("/") or "ewor.com" in href:
                full_url = href if "http" in href else f"https://www.ewor.com{href}"
                scrape_page(full_url)
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")

# Start scraping
for url in start_urls:
    scrape_page(url)

# Save the scraped data to a JSON file
with open("ewor_data.json", "w", encoding="utf-8") as f:
    json.dump(scraped_data, f, ensure_ascii=False, indent=2)

print(f"Scraping completed. Data saved to ewor_data.json.")
