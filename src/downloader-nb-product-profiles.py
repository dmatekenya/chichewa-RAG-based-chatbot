import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://www.natbank.co.mw"
START_URL = "https://www.natbank.co.mw/publications/product-profiles"

# Output folder
OUT_DIR = "/Users/dmatekenya/git-repos/rag-demo-chichewa/data/docs/national-bank-products"
os.makedirs(OUT_DIR, exist_ok=True)


def get_soup(url):
    """Return BeautifulSoup object for a URL."""
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")


def get_category_links():
    """Extract all category page links from the Product Profiles landing page."""
    soup = get_soup(START_URL)
    links = []

    for a in soup.select("a"):
        href = a.get("href", "")
        # Category pages look like: /publications/product-profiles/accounts
        if href.startswith("/publications/product-profiles/") and href.count("/") == 3:
            links.append(urljoin(BASE, href))

    return list(set(links))  # remove duplicates


def get_pdf_links(category_url):
    """Extract all PDF download links from a category page."""
    soup = get_soup(category_url)
    pdfs = []

    for a in soup.select("a"):
        href = a.get("href", "")
        if "file" in href and href.endswith("file"):
            # Example: /publications/.../some-file/file
            pdfs.append(urljoin(BASE, href))

    return pdfs


def download_file(url):
    """Download a single file with correct filename."""
    filename = url.split("/")[-2] + ".pdf"  # The final 'file' is not part of name
    path = os.path.join(OUT_DIR, filename)

    print(f"Downloading: {filename}")

    r = requests.get(url, timeout=60)
    r.raise_for_status()

    with open(path, "wb") as f:
        f.write(r.content)

    print(f"Saved → {path}")


def main():
    print("Collecting category pages...")
    categories = get_category_links()
    print(f"Found {len(categories)} categories")

    all_pdfs = []

    for cat in categories:
        print(f"\n⟹ Scanning category: {cat}")
        pdfs = get_pdf_links(cat)
        print(f"  Found {len(pdfs)} PDFs")
        all_pdfs.extend(pdfs)

    print(f"\nTotal PDFs found: {len(all_pdfs)}")

    for pdf_url in all_pdfs:
        download_file(pdf_url)

    print("\n✓ All files downloaded.")


if __name__ == "__main__":
    main()
