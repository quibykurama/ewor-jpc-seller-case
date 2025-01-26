import os
import requests
from bs4 import BeautifulSoup
import json

# Define output directories
OUTPUT_DIR = "ewor-scraper-output"
PDF_DIR = os.path.join(OUTPUT_DIR, "pdf")
JSON_DIR = os.path.join(OUTPUT_DIR, "json")

# Create directories
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(JSON_DIR, exist_ok=True)

# URLs to scrape
URLS = {
    "home": "https://www.ewor.com/",
    "fellow_login": "https://platform.ewor.com/auth/login/",
    "application_form": "https://www.ewor.com/apply?sc=EW&ssc=Header&sm=Direct",
    "legal_imprint": "https://www.ewor.com/legal/imprint",
    "legal_privacy_policy": "https://www.ewor.com/legal/privacy-policy",
    "legal_terms_conditions": "https://www.ewor.com/legal/terms-and-conditions",
    "founder_resources": "https://www.ewor.com/startup-templates?sc=EW&ssc=Header&sm=Direct",
    "team": "https://www.ewor.com/ewor-team",
    "ideation_fellowship_page": "https://www.ewor.com/ideation-fellowship",
    "traction_fellowship_page": "https://www.ewor.com/traction-fellowship",
    "nominations_form": "https://form.ewor.com/nominate",
    "faq": "https://www.ewor.com/faq",
    "mentor_onboard_form": "https://forms.ewor.com/onboarding",
    "blog": "https://www.ewor.com/blog",
    "investor_register_form": "https://form.ewor.com/investor-network-registration",
    "reminder_form": "https://reminder.ewor.com/",
    "collaborate_form": "https://forms.ewor.com/collaborate-with-ewor"
}

# PDF links
PDF_FILES = [
    ("https://downloads.ewor.com/decks/Ideation_Education_Pre-Investment_Agreement_2025.pdf", "ideation_fellowship_agreement.pdf"),
    ("https://downloads.ewor.com/EWOR%20Ideation%20Fellowship%20Factsheet.pdf", "ideation_fellowship_factsheet.pdf"),
    ("https://downloads.ewor.com/decks/2024-07-01_Traction_Fellowship_Agreement_guaranteed_investment_2024.pdf", "traction_fellowship_agreement.pdf"),
    ("https://downloads.ewor.com/EWOR%20Traction%20Fellowship%20Factsheet.pdf", "traction_fellowship_factsheet.pdf")
]

# Helper functions
def download_pdf(url, filename):
    """Download and save PDF files."""
    response = requests.get(url)
    if response.status_code == 200:
        filepath = os.path.join(PDF_DIR, filename)
        with open(filepath, "wb") as file:
            file.write(response.content)
        print(f"Downloaded PDF: {filename}")
    else:
        print(f"Failed to download PDF: {url}")

def scrape_page(url, output_filename, parser_func):
    """Scrape a single page and save the results to JSON."""
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        data = parser_func(soup)
        filepath = os.path.join(JSON_DIR, output_filename)
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        print(f"Scraped and saved: {output_filename}")
    else:
        print(f"Failed to scrape page: {url}")

# Parsing functions
def parse_blog_page(soup):
    """Parse a single blog page."""
    title = soup.title.string.strip() if soup.title else None
    description = soup.find("meta", {"name": "description"})["content"].strip() if soup.find("meta", {"name": "description"}) else None
    content = " ".join([p.get_text(strip=True) for p in soup.find_all("p")])
    return {
        "title": title,
        "description": description,
        "content": content
    }

def parse_blog_list(soup):
    """Parse the main blog list and return blog post links."""
    blogs = []
    for blog in soup.find_all("div", class_="blog_other-item"):
        title = blog.find("h2").get_text(strip=True)
        link = blog.find("a")["href"]
        blogs.append({"title": title, "link": f"https://www.ewor.com{link}"})
    return {"blogs": blogs}

def parse_founder_resources(soup):
    """Parse the Founder Resources page."""
    resources = []
    for resource in soup.find_all("a", class_="template_item"):
        name = resource.get_text(strip=True)
        link = resource["href"]
        resources.append({"name": name, "link": link})
    return {"resources": resources}

# Main scraper function
def main():
    # Download PDFs
    for url, filename in PDF_FILES:
        download_pdf(url, filename)

    # Scrape pages
    scrape_page(URLS["home"], "home.json", lambda soup: {"title": soup.title.string})
    scrape_page(URLS["blog"], "blog.json", parse_blog_list)
    scrape_page(URLS["founder_resources"], "founder_resources.json", parse_founder_resources)

    # Scrape blog posts
    blogs_data_path = os.path.join(JSON_DIR, "blog.json")
    if os.path.exists(blogs_data_path):
        with open(blogs_data_path, "r") as file:
            blogs = json.load(file)["blogs"]
            for blog in blogs:
                blog_filename = f"blog_{blog['title'].replace(' ', '_').lower()}.json"
                scrape_page(blog["link"], blog_filename, parse_blog_page)

if __name__ == "__main__":
    main()
