import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from tldextract import extract
import logging

logging.basicConfig(level=logging.INFO)

def is_same_domain(base, link):
    base_ext = extract(base)
    link_ext = extract(link)
    return (base_ext.domain == link_ext.domain) and (base_ext.suffix == link_ext.suffix)

def crawl_blog_urls(start_url, path_prefix=("/blog", "/blogs")):
    visited, to_visit = set(), {start_url}
    found_urls = set()

    while to_visit:
        url = to_visit.pop()
        if url.rstrip("/") in visited:
            continue
        visited.add(url.rstrip("/"))

        try:
            logging.info(f"Fetching: {url}")
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")
        except Exception as e:
            logging.warning(f"Failed to fetch {url}: {e}")
            continue

        for a in soup.find_all("a", href=True):
            link = urljoin(url, a["href"])
            if not is_same_domain(start_url, link):
                continue

            parsed = urlparse(link)
            if any(parsed.path.startswith(prefix) for prefix in path_prefix) and link not in found_urls:
                found_urls.add(link)
                to_visit.add(link)

    return sorted(found_urls)
