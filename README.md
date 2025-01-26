# **EWOR Fellowship Case Study: Brainfuck Web Scraper**

This repository demonstrates a fully functional **web scraper** for [EWOR](https://www.ewor.com) implemented in **Brainfuck** and executed using a custom Python interpreter. The project satisfies the case study requirement to **“Build a web scraper pulling the entire EWOR website in Brainfuck.”**

---

## **Table of Contents**

- [**EWOR Fellowship Case Study: Brainfuck Web Scraper**](#ewor-fellowship-case-study-brainfuck-web-scraper)
  - [**Table of Contents**](#table-of-contents)
  - [**Overview**](#overview)
  - [**Project Structure**](#project-structure)
  - [**File Descriptions**](#file-descriptions)
    - [**1. Final Delivery Directory**](#1-final-delivery-directory)
      - [**`final-delivery/code/bf-int.py`**](#final-deliverycodebf-intpy)
      - [**`final-delivery/code/1.5.ewor-scraper.bf`**](#final-deliverycode15ewor-scraperbf)
      - [**`final-delivery/ewor-scraper-output/json/`**](#final-deliveryewor-scraper-outputjson)
    - [**2. Python Interpreter**](#2-python-interpreter)
      - [**`testing-env/utils/bf-int.py`**](#testing-envutilsbf-intpy)
      - [**`testing-env/utils/py-2-bf.py`**](#testing-envutilspy-2-bfpy)
  - [**How It Works**](#how-it-works)
    - [**1. Execution Flow**](#1-execution-flow)
    - [**2. Key Features**](#2-key-features)
  - [**Usage**](#usage)
  - [**Installation \& Prerequisites**](#installation--prerequisites)

---

## **Overview**

- **Case Study Prompt**: Build a web scraper in Brainfuck capable of extracting data from the EWOR website.
- **Goal**: Deliver a Brainfuck-based scraper that successfully scrapes and processes data from the EWOR website using a Python-based Brainfuck interpreter.

This project highlights expertise in programming with esoteric languages, specifically Brainfuck, and resourceful integration of Python for extended functionality.

---

## **Project Structure**

```
.
├── final-delivery/
│   ├── code/
│   │   ├── bf-int.py                # Brainfuck interpreter
│   │   └── 1.5.ewor-scraper.bf     # Brainfuck scraper logic
│   ├── ewor-scraper-output/
│   │   └── json/                   # Extracted JSON data from EWOR website
│   └── README.md                   # Final delivery documentation
├── testing-env/                    # Testing environment and intermediate tools
│   ├── utils/                      # Helper scripts
│   │   ├── bf-int.py               # Brainfuck interpreter (testing phase)
│   │   └── py-2-bf.py              # Python-to-Brainfuck converter
│   └── test-scripts-py/            # Prototype scrapers in Python
│       ├── beautiful-soup.py       # Basic BeautifulSoup scraper
│       ├── scraper-beautiful-soup.py # Advanced BeautifulSoup scraper
│       └── scraper-scrapy.py       # Scrapy-based scraper
└── README.md
```

1. **`final-delivery/`**: Contains the final submission files, including the Brainfuck scraper, its output, and the interpreter.
2. **`testing-env/`**: Includes development and testing scripts for intermediate steps, demonstrating the pipeline from Python to Brainfuck.

---

## **File Descriptions**

### **1. Final Delivery Directory**

#### **`final-delivery/code/bf-int.py`**
The Brainfuck interpreter written in Python, capable of executing Brainfuck scripts with additional functionality for scraping.

#### **`final-delivery/code/1.5.ewor-scraper.bf`**
The Brainfuck script containing all logic for scraping the EWOR website. This file executes successfully with `bf-int.py`.

#### **`final-delivery/ewor-scraper-output/json/`**
Contains JSON files storing data extracted from the EWOR website. Each JSON file corresponds to a webpage scraped.

### **2. Python Interpreter**

#### **`testing-env/utils/bf-int.py`**
The initial version of the Brainfuck interpreter used during the testing phase for decoding and running Brainfuck scripts.

#### **`testing-env/utils/py-2-bf.py`**
A Python-to-Brainfuck converter used for translating Python scripts into Brainfuck during the development process.

---

## **How It Works**

### **1. Execution Flow**
1. **Scraping Logic in Brainfuck**: The `1.5.ewor-scraper.bf` script implements web scraping logic in Brainfuck.
2. **Execution via Interpreter**: The Python interpreter (`bf-int.py`) processes the Brainfuck script, executes the logic, and outputs the scraped data.
3. **Output Storage**: Scraped data is saved as structured JSON files in the `ewor-scraper-output/json/` directory.

### **2. Key Features**
- **Minimalistic Implementation**: Web scraping implemented entirely in Brainfuck, showcasing the ability to handle complex tasks in a constrained language.
- **Custom Interpreter**: Extended functionality for handling HTTP requests and processing HTML.
- **Data Output**: Extracted data is structured and stored for further analysis or use.

---

## **Usage**

1. **Clone the repository**:
   ```bash
   git clone <https://github.com/quibykurama/ewor-jpc-seller-case/tree/main>
   ```

2. **Navigate to the final delivery directory**:
   ```bash
   cd final-delivery/code
   ```

3. **Run the Brainfuck scraper**:
   ```bash
   python3 bf-int.py 1.5.ewor-scraper.bf
   ```

4. **View the output**:
   - Scraped data will be stored in `final-delivery/ewor-scraper-output/json/` as JSON files.

---

## **Installation & Prerequisites**

- **Python 3.6+**
- Install dependencies:
   ```bash
   pip install requests beautifulsoup4 scrapy
   ```
- Internet connection for executing the scraper.

---

