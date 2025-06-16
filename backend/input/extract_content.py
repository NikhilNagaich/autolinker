import requests
from readability import Document
from urllib.parse import urlparse
import logging

logging.basicConfig(level=logging.INFO)

def extract_blog_data(url):
    try:
        logging.info(f"Extracting content from: {url}")
        res = requests.get(url, timeout=10)
        res.raise_for_status()

        doc = Document(res.text)
        title = doc.title()
        html = doc.summary()

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        content = soup.get_text(separator="\n")

        slug = urlparse(url).path.rstrip("/").split("/")[-1]
        return {
            "url": url,
            "slug": slug,
            "title": title.strip(),
            "content": content.strip(),        # plain text
            "content_html": html               # original HTML
        }

    except Exception as e:
        logging.warning(f"Failed to extract from {url}: {e}")
        return None
