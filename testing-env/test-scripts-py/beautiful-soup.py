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