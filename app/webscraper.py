import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os

DATA_DIR = "app/data/raw"
os.makedirs(DATA_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

def get_all_sublinks(url, must_contain="loan", domain_only=True):
    """
    Extract all unique sublinks from a given URL, optionally filtering for keywords and domain.

    Args:
        url (str): The URL to scan for sublinks.
        must_contain (str, optional): Filter links to only those containing this substring. Defaults to "loan".
        domain_only (bool, optional): Only include links from the same domain. Defaults to True.

    Returns:
        List[str]: Sorted list of filtered sublinks.
    """
    resp = httpx.get(url, headers=HEADERS, follow_redirects=True)
    if resp.status_code != 200:
        print(f"Failed to fetch page: {resp.status_code}")
        return []

    soup = BeautifulSoup(resp.text, 'html.parser')
    links = set()

    root_domain = urlparse(url).netloc

    for tag in soup.find_all('a', href=True):
        full_link = urljoin(url, tag['href'])
        if domain_only and urlparse(full_link).netloc != root_domain:
            continue
        if must_contain and must_contain not in full_link.lower():
            continue
        links.add(full_link)
    return sorted(links)

def extract_clean_text(html):
    """
    Clean HTML content by removing navigation, scripts, and extract main textual content.

    Args:
        html (str): HTML source as a string.

    Returns:
        str: Cleaned text extracted from HTML.
    """
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup(['nav', 'footer', 'script', 'style', 'header', 'form']):
        tag.decompose()
    main_content = soup.find('div', class_='container') or soup.body
    text = main_content.get_text(separator='\n', strip=True)
    return text

def scrape_and_save_all(base_url):
    """
    Scrape all relevant subpages from a base URL, extract, clean, and save text to data/raw/.

    Args:
        base_url (str): The main loan products URL to crawl from.

    Side Effects:
        Saves .txt files to the raw data folder.
    """
    sublinks = get_all_sublinks(base_url)
    print(f"Found {len(sublinks)} loan-related links.")

    for url in sublinks:
        try:
            resp = httpx.get(url, headers=HEADERS, follow_redirects=True)
            if resp.status_code == 200:
                text = extract_clean_text(resp.text)
                fname = urlparse(url).path.replace('/', '_').strip('_') or "index"
                with open(f"{DATA_DIR}/{fname}.txt", "w", encoding="utf-8") as f:
                    f.write(text)
                print(f"Saved: {url}")
            else:
                print(f"Failed: {url} [{resp.status_code}]")
        except Exception as e:
            print(f"Error scraping {url}: {e}")

if __name__ == "__main__":
    base_url = "https://bankofmaharashtra.in/retail-loans"
    scrape_and_save_all(base_url)
