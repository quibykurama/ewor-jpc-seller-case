import os
import json
import re
from bs4 import BeautifulSoup

# Output directories
OUTPUT_DIR = "ewor-scraper-output"
PDF_DIR = os.path.join(OUTPUT_DIR, "pdf")
JSON_DIR = os.path.join(OUTPUT_DIR, "json")
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(JSON_DIR, exist_ok=True)

# PDF files
PDF_FILES = [
    ("https://downloads.ewor.com/decks/Ideation_Education_Pre-Investment_Agreement_2025.pdf", "ideation_fellowship_agreement.pdf"),
    ("https://downloads.ewor.com/EWOR%20Ideation%20Fellowship%20Factsheet.pdf", "ideation_fellowship_factsheet.pdf"),
    ("https://downloads.ewor.com/decks/2024-07-01_Traction_Fellowship_Agreement_guaranteed_investment_2024.pdf", "traction_fellowship_agreement.pdf"),
    ("https://downloads.ewor.com/EWOR%20Traction%20Fellowship%20Factsheet.pdf", "traction_fellowship_factsheet.pdf")
]

def sanitize_filename(filename):
    """Sanitize filenames to be OS-friendly."""
    return re.sub(r"[<>:\"/\\|?*']", "_", filename).strip()

def download_pdf(url, filename):
    """Download and save PDF files."""
    print(f"Downloading PDF: {filename} (URL: {url})")
    filepath = os.path.join(PDF_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(b"PDF download simulation")  # Mock for testing

def parse_html_file(filepath, parser_func):
    """Parse an HTML file using the specified parser function."""
    print(f"Parsing: {filepath}")
    with open(filepath, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
        return parser_func(soup)

# Parsing Functions
def parse_home_page(soup):
    return {"title": soup.title.string.strip(), "sections": ["Meet Our Fellows", "The EWOR Edge"]}

def parse_fellow_login(soup):
    return {"title": soup.title.string.strip(), "form_fields": ["Email", "Password"]}

def parse_application_form(soup):
    return {"title": soup.title.string.strip(), "form_url": "https://form.ewor.com/apply"}

def parse_legal_page(soup):
    return {"title": soup.title.string.strip(), "content": "Legal content"}

def parse_founder_resources(soup):
    resources = [{"name": "Template", "description": "A great template", "link": "https://example.com/resource"}]
    return {"resources": resources}

def parse_team_page(soup):
    return {"title": "Team Page", "team_members": ["Member 1", "Member 2"]}

def parse_fellowship_page(soup):
    return {"title": "Fellowship", "key_features": {"funding": "€150K investment"}}

def parse_nominations_form(soup):
    return {"title": "Nominations Form", "fields": ["First Name", "Last Name", "Email"]}

def parse_faq(soup):
    faqs = [{"question": "What is EWOR?", "answer": "A platform for aspiring entrepreneurs."}]
    return {"faqs": faqs}

def parse_blog_list(soup):
    blogs = [{"title": "Blog Post 1", "link": "https://www.ewor.com/blog/post1"}]
    return {"blogs": blogs}

def parse_blog_page(soup):
    return {"title": soup.title.string.strip(), "content": "Blog content sample"}

def parse_investor_register_form(soup):
    return {"title": "Investor Register Form", "fields": ["Name", "Email", "Phone"]}

def parse_reminder_form(soup):
    return {"title": "Reminder Form", "fields": ["Email"]}

def parse_collaborate_form(soup):
    return {"title": "Collaborate Form", "fields": ["First Name", "Last Name", "Email"]}

# Main Function
def main():
    # Download PDFs
    for url, filename in PDF_FILES:
        download_pdf(url, filename)

    # HTML file mapping
    html_files = {
        "home": ("../ewor-htm/home.html", parse_home_page),
        "fellow_login": ("../ewor-htm/fellow-login.html", parse_fellow_login),
        "application_form": ("../ewor-htm/application-form.html", parse_application_form),
        "legal_imprint": ("../ewor-htm/legal-imprint.html", parse_legal_page),
        "legal_privacy_policy": ("../ewor-htm/privacy-policy.html", parse_legal_page),
        "legal_terms_conditions": ("../ewor-htm/terms-conditions.html", parse_legal_page),
        "founder_resources": ("../ewor-htm/founder-resources.html", parse_founder_resources),
        "team": ("../ewor-htm/team.html", parse_team_page),
        "ideation_fellowship_page": ("../ewor-htm/ideation-fellowship-page.html", parse_fellowship_page),
        "traction_fellowship_page": ("../ewor-htm/traction-fellowship-page.html", parse_fellowship_page),
        "nominations_form": ("../ewor-htm/nominatins-form.html", parse_nominations_form),
        "faq": ("../ewor-htm/faq.html", parse_faq),
        "blog": ("../ewor-htm/blog.html", parse_blog_list),
        "investor_register_form": ("../ewor-htm/investor-register-form.html", parse_investor_register_form),
        "reminder_form": ("../ewor-htm/reminder-form.html", parse_reminder_form),
        "collaborate_form": ("../ewor-htm/collaborate-form.html", parse_collaborate_form),
    }

    # Parse and save JSON
    for key, (filepath, parser_func) in html_files.items():
        try:
            result = parse_html_file(filepath, parser_func)
            output_filepath = os.path.join(JSON_DIR, f"{key}.json")
            with open(output_filepath, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"Saved JSON: {output_filepath}")
        except Exception as e:
            print(f"Failed to process {key}: {e}")

if __name__ == "__main__":
    main()
