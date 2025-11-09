# crawler.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://www.un.org/en/about-us"

def crawl_site(url=BASE_URL, max_pages=5):
    visited = set()
    pages = []
    to_visit = [url]

    while to_visit and len(pages) < max_pages:
        link = to_visit.pop(0)
        if link in visited:
            continue

        print(f"Crawling: {link}")
        visited.add(link)

        try:
            html = requests.get(link, timeout=10).text
            soup = BeautifulSoup(html, "html.parser")

            # collect text
            text = " ".join([p.get_text() for p in soup.find_all("p")])
            pages.append({"url": link, "content": text})

            # find more internal links
            for a in soup.find_all("a", href=True):
                new_link = urljoin(BASE_URL, a["href"])
                if "un.org/en" in new_link and new_link not in visited:
                    to_visit.append(new_link)

        except Exception as e:
            print("Error:", e)

    return pages

if __name__ == "__main__":
    data = crawl_site()
    print(f"Crawled {len(data)} pages.")
