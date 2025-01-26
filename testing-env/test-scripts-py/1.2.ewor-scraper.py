import requests
from bs4 import BeautifulSoup
import json
import os

# Create output directory
os.makedirs("output", exist_ok=True)

# Pages to scrape
pages = {
    "home": "https://www.ewor.com/",
    "fellow_login": "https://platform.ewor.com/auth/login/",
    "application_form": "https://www.ewor.com/apply?sc=EW&ssc=Header&sm=Direct",
    "legal_imprint": "https://www.ewor.com/legal/imprint",
    "legal_privacy_policy": "https://www.ewor.com/legal/privacy-policy",
    "legal_terms_conditions": "https://www.ewor.com/legal/terms-and-conditions",
    "founder_resources": "https://www.ewor.com/startup-templates?sc=EW&ssc=Header&sm=Direct",
    "team": "https://www.ewor.com/ewor-team",
    "ideation_fellowship_page": "https://www.ewor.com/ideation-fellowship",
    "ideation_fellowship_agreement": "https://downloads.ewor.com/decks/Ideation_Education_Pre-Investment_Agreement_2025.pdf",
    "ideation_fellowship_factsheet": "https://downloads.ewor.com/EWOR%20Ideation%20Fellowship%20Factsheet.pdf",
    "traction_fellowship_page": "https://www.ewor.com/traction-fellowship",
    "traction_fellowship_agreement": "https://downloads.ewor.com/decks/2024-07-01_Traction_Fellowship_Agreement_guaranteed_investment_2024.pdf",
    "traction_fellowship_factsheet": "https://downloads.ewor.com/EWOR%20Traction%20Fellowship%20Factsheet.pdf",
    "nominations_form": "https://form.ewor.com/nominate",
    "faq": "https://www.ewor.com/faq",
    "mentor_onboard_form": "https://forms.ewor.com/onboarding",
    "blog": "https://www.ewor.com/blog",
    "investor_register_form": "https://form.ewor.com/investor-network-registration",
    "reminder_form": "https://reminder.ewor.com/",
    "collaborate_form": "https://forms.ewor.com/collaborate-with-ewor",
}

def scrape_html_page(url, output_file):
    """Scrapes general HTML pages."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract data
        title = soup.title.string.strip() if soup.title else "No title"
        meta_description = soup.find("meta", {"name": "description"})
        meta_description = meta_description["content"].strip() if meta_description else "No description"
        content = " ".join([p.get_text(strip=True) for p in soup.find_all("p")])

        # Save data to a JSON file
        data = {"url": url, "title": title, "meta_description": meta_description, "content": content}
        with open(f"output/{output_file}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Scraped and saved: {output_file}.json")
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")

def scrape_pdf(url, output_file):
    """Downloads and saves PDF files."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        pdf_path = f"output/{output_file}.pdf"
        with open(pdf_path, "wb") as f:
            f.write(response.content)
        print(f"Downloaded PDF: {output_file}.pdf")
    except Exception as e:
        print(f"Failed to download PDF {url}: {e}")

# Scrape all pages
for page_name, url in pages.items():
    if url.endswith(".pdf"):
        scrape_pdf(url, page_name)
    else:
        scrape_html_page(url, page_name)
