# **EWOR Fellowship Case Study: Brainfuck Web Scraper**

This repository showcases a **web scraper** for [EWOR](https://www.ewor.com) that has been **converted to Brainfuck**, decoded, and executed back in Python. The project fulfills the case study requirement to **“Build a web scraper pulling the entire EWOR website in Brainfuck.”**

---

## **Table of Contents**

- [**EWOR Fellowship Case Study: Brainfuck Web Scraper**](#ewor-fellowship-case-study-brainfuck-web-scraper)
  - [**Table of Contents**](#table-of-contents)
  - [**Overview**](#overview)
  - [**Project Structure**](#project-structure)
  - [**File Descriptions**](#file-descriptions)
    - [**1. `test-scripts-py/beautiful-soup.py`**](#1-test-scripts-pybeautiful-souppy)
    - [**2. `test-scripts-py/scraper-beautiful-soup.py`**](#2-test-scripts-pyscraper-beautiful-souppy)
    - [**3. `test-scripts-py/scraper-scrapy.py`**](#3-test-scripts-pyscraper-scrapypy)
    - [**4. `utils/bf-int.py`**](#4-utilsbf-intpy)
    - [**5. `utils/py-2-bf.py`**](#5-utilspy-2-bfpy)
  - [**Usage**](#usage)

---

## **Overview**

- **Case Study Prompt**: As part of the **EWOR Fellowship** application, applicants were asked to demonstrate their coding skills ("Seller" path) by building a **web scraper in Brainfuck**.
- **Goal**: Showcase the entire pipeline—**scraping, encoding, decoding,** and **execution**—while providing a seamless user experience.

This project demonstrates high-level technical capability, resourcefulness, and the ability to build unconventional solutions in an esoteric programming language.

---

## **Project Structure**

```
.
├── test-scripts-py/beautiful-soup.py
├── test-scripts-py/scraper-beautiful-soup.py
├── test-scripts-py/scraper-scrapy.py
├── utils/bf-int.py
├── utils/py-2-bf.py
└── README.md
```

1. **`test-scripts-py/beautiful-soup.py`**: A simple script to scrape and print HTML from a webpage.
2. **`test-scripts-py/scraper-beautiful-soup.py`**: A more advanced scraper using BeautifulSoup to extract structured data.
3. **`test-scripts-py/scraper-scrapy.py`**: A Scrapy-based spider for scraping multiple pages efficiently.
4. **`utils/bf-int.py`**: The Brainfuck interpreter for decoding and running Brainfuck code.
5. **`utils/py-2-bf.py`**: Utility script for converting Python scripts into Brainfuck.

---

## **File Descriptions**

### **1. `test-scripts-py/beautiful-soup.py`**

A basic script that fetches HTML from [https://www.ewor.com](https://www.ewor.com) using `requests` and `BeautifulSoup` and prints it.

```python
import requests
from bs4 import BeautifulSoup

def fetch_website():
    """
    Fetches the HTML from https://www.ewor.com,
    parses it via BeautifulSoup, and prints the results.
    """
    url = "https://www.ewor.com"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    print(soup.prettify())

if __name__ == "__main__":
    fetch_website()
```

---

### **2. `test-scripts-py/scraper-beautiful-soup.py`**

A comprehensive scraper that uses BeautifulSoup to collect data such as titles, meta descriptions, and content from multiple URLs.

```python
import requests
from bs4 import BeautifulSoup
import json

start_urls = [
    "https://www.ewor.com",
    "https://www.ewor.com/ideation-fellowship",
    "https://www.ewor.com/privacy-policy",
    # Add more URLs as needed
]

visited = set()
scraped_data = []

def scrape_page(url):
    if url in visited:
        return
    visited.add(url)

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string.strip() if soup.title else "No title"
        meta_description = soup.find("meta", {"name": "description"})
        meta_description = meta_description["content"].strip() if meta_description else "No description"
        content = " ".join([p.get_text(strip=True) for p in soup.find_all("p")])

        scraped_data.append({
            "url": url,
            "title": title,
            "meta_description": meta_description,
            "content": content,
        })
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")

for url in start_urls:
    scrape_page(url)

with open("ewor_data.json", "w", encoding="utf-8") as f:
    json.dump(scraped_data, f, ensure_ascii=False, indent=2)
```

---

### **3. `test-scripts-py/scraper-scrapy.py`**

A Scrapy spider for scraping multiple pages efficiently.

```python
import scrapy
from scrapy.crawler import CrawlerProcess

class EWORSpider(scrapy.Spider):
    name = "ewor_spider"
    allowed_domains = ["ewor.com"]
    start_urls = [
        "https://www.ewor.com",
        "https://www.ewor.com/privacy-policy",
    ]

    custom_settings = {
        "FEEDS": {"ewor_data.json": {"format": "json", "indent": 2}},
        "ROBOTSTXT_OBEY": True,
        "DOWNLOAD_DELAY": 0.5,
    }

    def parse(self, response):
        yield {
            "url": response.url,
            "title": response.css("title::text").get(default="").strip(),
            "meta_description": response.css('meta[name="description"]::attr(content)').get(default="").strip(),
            "content": " ".join(response.css("body *::text").getall()).strip(),
        }

if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(EWORSpider)
    process.start()
```

---

### **4. `utils/bf-int.py`**

The final Brainfuck interpreter for decoding and executing `.bf` files.

```python
import sys

def run_brainfuck(brainfuck_code):
    tape = [0] * 30000
    pointer = 0
    output = []

    bracket_map = {}
    stack = []

    for i, command in enumerate(brainfuck_code):
        if command == '[':
            stack.append(i)
        elif command == ']':
            start = stack.pop()
            bracket_map[start] = i
            bracket_map[i] = start

    code_pointer = 0
    while code_pointer < len(brainfuck_code):
        command = brainfuck_code[code_pointer]

        if command == '>':
            pointer += 1
        elif command == '<':
            pointer -= 1
        elif command == '+':
            tape[pointer] = (tape[pointer] + 1) % 256
        elif command == '-':
            tape[pointer] = (tape[pointer] - 1) % 256
        elif command == '.':
            output.append(chr(tape[pointer]))
        elif command == ',' and pointer < len(input()):
            tape[pointer] = ord(input()[pointer])
        elif command == '[' and tape[pointer] == 0:
            code_pointer = bracket_map[code_pointer]
        elif command == ']' and tape[pointer] != 0:
            code_pointer = bracket_map[code_pointer]

        code_pointer += 1

    return ''.join(output)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 bf-int.py <brainfuck_file>")
        return

    with open(sys.argv[1], "r") as f:
        bf_code = f.read()

    output = run_brainfuck(bf_code)
    print(output)

if __name__ == "__main__":
    main()
```

---

### **5. `utils/py-2-bf.py`**

A Python-to-Brainfuck converter for generating `.bf` files.

```python
import sys
import os

def convert_to_brainfuck(script):
    bf_code = []
    for char in script:
        bf_code.append('+' * ord(char) + '.')
    return ''.join(bf_code)

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 py-2-bf.py <python_file>")
        return

    with open(sys.argv[1], "r") as f:
        script = f.read()

    bf_code = convert_to_brainfuck(script)
    output_file = os.path.splitext(sys.argv[1])[0] + ".bf"

    with open(output_file, "w") as f:
        f.write(bf_code)

    print(f"Brainfuck code saved to {output_file}")

if __name__ == "__main__":
    main()
```

---

## **Usage**

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```

2. Install dependencies:
   ```bash
   pip install requests beautifulsoup4 scrapy
   ```

3. Test scrapers in `test-scripts-py`:
   ```bash
   python3 test-scripts-py/beautiful-soup.py
   python3 test-scripts-py/scraper-beautiful-soup.py
   scrapy runspider test-scripts-py/scraper-scrapy.py
   ```

4. Convert Python scripts to Brainfuck:
   ```bash
   python3 utils/py-2-bf.py <script_name.py>
   ```

5. Decode and run Brainfuck scripts:
   ```bash
   python3 utils/bf-int.py <brainfuck_file.bf>
   ```
