import os
import json
import requests
from bs4 import BeautifulSoup
import re

# Directory setup
OUTPUT_DIR = "ewor-scraper-output"
PDF_DIR = os.path.join(OUTPUT_DIR, "pdf")
JSON_DIR = os.path.join(OUTPUT_DIR, "json")
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(JSON_DIR, exist_ok=True)

# URLs and PDF Files
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
    "blog": "https://www.ewor.com/blog",
    "investor_register_form": "https://form.ewor.com/investor-network-registration",
}

PDF_FILES = [
    ("https://downloads.ewor.com/decks/Ideation_Education_Pre-Investment_Agreement_2025.pdf", "ideation_fellowship_agreement.pdf"),
    ("https://downloads.ewor.com/EWOR%20Ideation%20Fellowship%20Factsheet.pdf", "ideation_fellowship_factsheet.pdf"),
    ("https://downloads.ewor.com/decks/2024-07-01_Traction_Fellowship_Agreement_guaranteed_investment_2024.pdf", "traction_fellowship_agreement.pdf"),
    ("https://downloads.ewor.com/EWOR%20Traction%20Fellowship%20Factsheet.pdf", "traction_fellowship_factsheet.pdf"),
]

# Utility Functions
def sanitize_filename(filename):
    """Sanitize filenames to be OS-friendly."""
    return re.sub(r"[<>:\"/\\|?*']", "_", filename).strip()

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

def scrape_page(url, parser_func):
    """Scrape a single page and return parsed data."""
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        return parser_func(soup)
    else:
        print(f"Failed to scrape URL: {url}")
        return None

# Parsing Functions for Each Page
def parse_home(soup):
    """Parse the Home page."""
    # Metadata
    title = soup.title.string.strip()
    meta_description = soup.find("meta", {"name": "description"})["content"].strip()
    og_image = soup.find("meta", {"property": "og:image"})["content"] if soup.find("meta", {"property": "og:image"}) else None

    # Hero Section
    hero_heading = soup.select_one(".home-hero_header h1").get_text(strip=True)
    hero_subheading = soup.select_one(".text-size-xl.is-hero").get_text(strip=True)
    hero_ctas = [{"text": a.get_text(strip=True), "link": a["href"]} for a in soup.select(".button-group a")]

    # Meet Our Fellows
    fellows = []
    for fellow in soup.select(".supported-slider_item"):
        name = fellow.select_one(".badge.is-grey div").get_text(strip=True)
        role = fellow.select_one(".fellows-header").get_text(strip=True)
        description = fellow.select_one(".fellows-paragraph p").get_text(strip=True)
        fellows.append({"name": name, "role": role, "description": description})

    # The EWOR Edge
    ewor_edge = [{"metric": item.select_one(".heading-style-h2").get_text(strip=True),
                  "description": item.select_one("p").get_text(strip=True)}
                 for item in soup.select(".ewor_item")]

    # For Founders by Founders
    founders = []
    for founder in soup.select(".founders_item"):
        name = founder.select_one("h3").get_text(strip=True)
        description = founder.select_one(".founders-text").get_text(strip=True)
        linkedin = founder.select_one("a[href*='linkedin']")["href"] if founder.select_one("a[href*='linkedin']") else None
        founders.append({"name": name, "description": description, "linkedin": linkedin})

    # Unicorn Founders and Investors
    investors = []
    for investor in soup.select(".investors_item"):
        name = investor.select_one(".investors_item-header div").get_text(strip=True)
        linkedin = investor.select_one("a[href*='linkedin']")["href"] if investor.select_one("a[href*='linkedin']") else None
        investors.append({"name": name, "linkedin": linkedin})

    # Footer Links
    footer_links = [{"text": a.get_text(strip=True), "link": a["href"]} for a in soup.select("footer a[href]")]

    return {
        "title": title,
        "meta_description": meta_description,
        "og_image": og_image,
        "hero_section": {
            "heading": hero_heading,
            "subheading": hero_subheading,
            "calls_to_action": hero_ctas,
        },
        "meet_our_fellows": fellows,
        "the_ewor_edge": ewor_edge,
        "for_founders_by_founders": founders,
        "unicorn_founders_and_investors": investors,
        "footer_links": footer_links,
    }


def parse_fellow_login(soup):
    """Parse the Fellow Login page."""
    form_fields = []
    for label in soup.select("label.ewor-input"):
        field_name = label.find("span").get_text(strip=True)
        field_type = label.find("input")["type"] if label.find("input") else None
        placeholder = label.find("input")["placeholder"] if label.find("input") else None
        form_fields.append({"name": field_name, "type": field_type, "placeholder": placeholder})

    footer_links = [
        {"text": a.get_text(strip=True), "link": a["href"]}
        for a in soup.select("footer a[href]")
    ]

    return {
        "title": soup.title.string.strip(),
        "meta_description": soup.find("meta", {"name": "description"})["content"].strip() if soup.find("meta", {"name": "description"}) else None,
        "form_fields": form_fields,
        "footer_links": footer_links
    }


def parse_application_form(soup):
    """Parse the Application Form page."""
    form_url = soup.find("iframe")["src"] if soup.find("iframe") else None
    return {
        "title": soup.title.string.strip(),
        "meta_description": soup.find("meta", {"name": "description"})["content"].strip(),
        "form_url": form_url
    }

def parse_legal_page(soup):
    """Parse any Legal page."""
    content = " ".join([p.get_text(strip=True) for p in soup.select("body p")])
    return {
        "title": soup.title.string.strip(),
        "content": content
    }

def parse_founder_resources(soup):
    """Parse the Founder Resources page."""
    resources = []
    for category in soup.select(".template_accordion"):
        category_name = category.select_one(".template_question").get_text(strip=True)
        templates = []
        for item in category.select(".template_item"):
            name = item.select_one("h3").get_text(strip=True)
            description = item.select_one(".text-size-s").get_text(strip=True)
            link = item["href"]
            templates.append({"name": name, "description": description, "link": link})
        resources.append({"category": category_name, "templates": templates})

    return {
        "title": soup.title.string.strip(),
        "meta_description": soup.find("meta", {"name": "description"})["content"].strip(),
        "resources": resources,
    }


def parse_team_page(soup):
    """Parse the Team page."""
    hero_section = {
        "heading": soup.select_one(".hero_component h1").get_text(strip=True),
        "cta": {
            "text": soup.select_one(".hero_component .button").get_text(strip=True),
            "link": soup.select_one(".hero_component .button")["href"]
        }
    }
    team_members = []
    for member in soup.select(".team_list .team_item"):
        name = member.select_one("h3").get_text(strip=True)
        role = member.select_one(".team_position").get_text(strip=True)
        linkedin = member.select_one(".team_linkedin a")["href"] if member.select_one(".team_linkedin a") else None
        description = member.select_one("p").get_text(strip=True)
        team_members.append({
            "name": name,
            "role": role,
            "linkedin": linkedin,
            "description": description
        })
    return {
        "title": soup.title.string.strip(),
        "meta_description": soup.find("meta", {"name": "description"})["content"].strip(),
        "hero_section": hero_section,
        "team_members": team_members
    }


def parse_ideation_fellowship_page(soup):
    """Parse the Ideation Fellowship page."""
    hero_section = {
        "title": soup.select_one(".hero_component h1").get_text(strip=True),
        "description": soup.select_one(".hero_component p").get_text(strip=True) if soup.select_one(".hero_component p") else None,
        "cta": {
            "text": soup.select_one(".hero_component .button").get_text(strip=True),
            "link": soup.select_one(".hero_component .button")["href"]
        }
    }
    key_features = [
        {
            "feature": feature.select_one(".heading-style-h3").get_text(strip=True),
            "description": feature.select_one("p").get_text(strip=True)
        }
        for feature in soup.select(".features_component .feature-item")
    ]
    return {
        "title": soup.title.string.strip(),
        "meta_description": soup.find("meta", {"name": "description"})["content"].strip(),
        "hero_section": hero_section,
        "key_features": key_features
    }

def parse_ideation_fellowship_page(soup):
    """Parse the Ideation Fellowship page."""
    hero_section = {
        "title": soup.select_one(".hero_component h1").get_text(strip=True),
        "description": soup.select_one(".hero_component p").get_text(strip=True) if soup.select_one(".hero_component p") else None,
        "cta": {
            "text": soup.select_one(".hero_component .button").get_text(strip=True),
            "link": soup.select_one(".hero_component .button")["href"]
        }
    }
    key_features = [
        {
            "feature": feature.select_one(".heading-style-h3").get_text(strip=True),
            "description": feature.select_one("p").get_text(strip=True)
        }
        for feature in soup.select(".features_component .feature-item")
    ]
    return {
        "title": soup.title.string.strip(),
        "meta_description": soup.find("meta", {"name": "description"})["content"].strip(),
        "hero_section": hero_section,
        "key_features": key_features
    }


def parse_nominations_form(soup):
    """Parse the Nominations Form page."""
    fields = []
    for field in soup.select(".fillout-field"):
        label = field.find("label").get_text(strip=True) if field.find("label") else None
        input_type = field.find("input")["type"] if field.find("input") else "text"
        placeholder = field.find("input")["placeholder"] if field.find("input") and "placeholder" in field.find("input").attrs else None
        required = field.find("span", class_="fillout-required-asterisk") is not None
        fields.append({"name": label, "type": input_type, "placeholder": placeholder, "required": required})

    return {
        "title": soup.title.string.strip(),
        "meta_description": soup.find("meta", {"name": "description"})["content"].strip(),
        "fields": fields,
    }


def parse_faq_page(soup):
    """Parse the FAQ page."""
    faqs = []
    for category in soup.select(".template_list-grid.is-faq"):
        category_name = category.select_one(".template_question.is-faq h2").get_text(strip=True)
        questions = [
            {
                "question": question.select_one(".faq_question h3").get_text(strip=True),
                "answer": question.select_one(".faq_answer p").get_text(strip=True)
            }
            for question in category.select(".faq_accordion")
        ]
        faqs.append({"category": category_name, "questions": questions})
    return {
        "title": soup.title.string.strip(),
        "meta_description": soup.find("meta", {"name": "description"})["content"].strip(),
        "faqs": faqs
    }


def parse_investor_register_form(soup):
    """Parse the Investor Register Form page."""
    fields = []
    for field in soup.select(".fillout-field"):
        name = field.select_one(".fillout-field-label div").get_text(strip=True)
        placeholder = field.find("input")["placeholder"] if field.find("input") and "placeholder" in field.find("input").attrs else None
        required = field.find("span", class_="fillout-required-asterisk") is not None
        fields.append({"name": name, "placeholder": placeholder, "required": required})

    return {
        "title": soup.title.string.strip(),
        "meta_description": soup.find("meta", {"name": "description"})["content"].strip(),
        "fields": fields,
    }


def parse_reminder_form(soup):
    """Parse the Reminder Form page."""
    fields = []
    for field in soup.select(".tally-block-input-text, .tally-block-multiple-choice-option"):
        name = field.find_previous("h3").get_text(strip=True) if field.find_previous("h3") else None
        options = [opt.get_text(strip=True) for opt in field.select("label")] if field.select("label") else None
        fields.append({"name": name, "options": options})

    return {
        "title": soup.title.string.strip(),
        "meta_description": soup.find("meta", {"name": "description"})["content"].strip(),
        "fields": fields,
    }


def parse_collaborate_form(soup):
    """Parse the Collaborate Form page."""
    fields = []
    for field in soup.select(".tally-block-input-text, .tally-block-textarea"):
        name = field.find_previous("h3").get_text(strip=True) if field.find_previous("h3") else None
        required = field.find("span", class_="tally-required-indicator") is not None
        fields.append({"name": name, "required": required})

    return {
        "title": soup.title.string.strip(),
        "meta_description": soup.find("meta", {"name": "description"})["content"].strip(),
        "fields": fields,
    }

def parse_mentor_onboard_form(soup):
    """Parse the Mentor Onboarding Form page."""
    fields = []
    for field in soup.select(".tally-block-input-text, .tally-block-textarea"):
        name = field.find_previous("h3").get_text(strip=True) if field.find_previous("h3") else None
        required = field.find("span", class_="tally-required-indicator") is not None
        fields.append({"name": name, "required": required})

    return {
        "title": soup.title.string.strip(),
        "meta_description": soup.find("meta", {"name": "description"})["content"].strip(),
        "fields": fields,
    }

def parse_blog_list(soup):
    """Parse the Blog list page."""
    blogs = []
    for blog in soup.select(".blog_other-item"):
        title = blog.find("h2").get_text(strip=True)
        category = blog.find(".badge").get_text(strip=True) if blog.find(".badge") else None
        date = blog.find("div", {"class": None}).get_text(strip=True)
        image = blog.find("img")["src"] if blog.find("img") else None
        link = blog.find("a")["href"]
        blogs.append({"title": title, "category": category, "date": date, "image": image, "link": link})

    return {
        "title": soup.title.string.strip(),
        "meta_description": soup.find("meta", {"name": "description"})["content"].strip(),
        "blogs": blogs,
    }

def parse_blog_list(soup):
    """Parse the Blog list page."""
    blogs = []
    for blog in soup.select(".blog_other-item"):
        title = blog.find("h2").get_text(strip=True)
        category = blog.find(".badge").get_text(strip=True) if blog.find(".badge") else None
        date = blog.find("div", {"class": None}).get_text(strip=True)
        image = blog.find("img")["src"] if blog.find("img") else None
        link = blog.find("a")["href"]
        blogs.append({"title": title, "category": category, "date": date, "image": image, "link": link})

    return {
        "title": soup.title.string.strip(),
        "meta_description": soup.find("meta", {"name": "description"})["content"].strip(),
        "blogs": blogs,
    }

def parse_privacy_policy(soup):
    """Parse the Privacy Policy page."""
    sections = []
    for section in soup.select(".text-rich-text h3"):
        section_title = section.get_text(strip=True)
        section_content = " ".join([p.get_text(strip=True) for p in section.find_next_siblings("p")])
        sections.append({"title": section_title, "content": section_content})

    return {
        "title": soup.title.string.strip(),
        "meta_description": soup.find("meta", {"name": "description"})["content"].strip(),
        "sections": sections,
    }

def parse_legal_imprint(soup):
    """Parse the Legal Imprint page."""
    content = " ".join([p.get_text(strip=True) for p in soup.select(".text-rich-text p")])
    footer_links = [
        {"text": a.get_text(strip=True), "link": a["href"]}
        for a in soup.select("footer a[href]")
    ]
    return {
        "title": soup.title.string.strip(),
        "meta_description": soup.find("meta", {"name": "description"})["content"].strip(),
        "content": content,
        "footer_links": footer_links
    }

def parse_application_form(soup):
    """Parse the Application Form page."""
    form_url = soup.select_one("iframe")["src"] if soup.select_one("iframe") else None
    countdown = {
        "days": soup.select_one("#days").get_text(strip=True) if soup.select_one("#days") else "N/A",
        "hours": soup.select_one("#hours").get_text(strip=True) if soup.select_one("#hours") else "N/A",
        "minutes": soup.select_one("#minutes").get_text(strip=True) if soup.select_one("#minutes") else "N/A",
        "seconds": soup.select_one("#seconds").get_text(strip=True) if soup.select_one("#seconds") else "N/A",
    }
    footer_links = [
        {"text": a.get_text(strip=True), "link": a["href"]}
        for a in soup.select("footer a[href]")
    ]
    return {
        "title": soup.title.string.strip(),
        "meta_description": soup.find("meta", {"name": "description"})["content"].strip(),
        "form_url": form_url,
        "countdown": countdown,
        "footer_links": footer_links
    }

def parse_terms_conditions(soup):
    """Parse the Terms & Conditions page."""
    sections = []
    for section in soup.select(".text-rich-text h3"):
        title = section.get_text(strip=True)
        content = " ".join([p.get_text(strip=True) for p in section.find_next_siblings("p")])
        sections.append({"title": title, "content": content})

    footer_links = [
        {"text": a.get_text(strip=True), "link": a["href"]}
        for a in soup.select("footer a[href]")
    ]
    return {
        "title": soup.title.string.strip(),
        "meta_description": soup.find("meta", {"name": "description"})["content"].strip(),
        "sections": sections,
        "footer_links": footer_links
    }


# Main Function
def main():
    # Download PDFs
    for url, filename in PDF_FILES:
        download_pdf(url, filename)

    # Scrape pages and save JSON
    for key, url in URLS.items():
        parser_func = globals().get(f"parse_{key}", None)
        if parser_func:
            data = scrape_page(url, parser_func)
            if data:
                output_path = os.path.join(JSON_DIR, f"{key}.json")
                with open(output_path, "w", encoding="utf-8") as file:
                    json.dump(data, file, ensure_ascii=False, indent=2)
                print(f"Saved JSON: {output_path}")

if __name__ == "__main__":
    main()
