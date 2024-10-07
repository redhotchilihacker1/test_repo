import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

class SimpleSpider:
    def __init__(self, start_url, max_pages):
        self.start_url = start_url
        self.max_pages = max_pages
        self.visited = set()
        self.to_visit = [start_url]

    def crawl(self):
        while self.to_visit and len(self.visited) < self.max_pages:
            url = self.to_visit.pop(0)
            if url not in self.visited:
                self.visit(url)

    def visit(self, url):
        try:
            print(f"Visiting: {url}")
            response = requests.get(url)
            if response.status_code == 200:
                self.visited.add(url)
                self.extract_links(response.text, url)
            else:
                print(f"Failed to retrieve: {url} (status code: {response.status_code})")
        except requests.RequestException as e:
            print(f"Error visiting {url}: {e}")

        time.sleep(1)  # Sayfalar arasında bekleme

    def extract_links(self, html, base_url):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a', href=True):
            full_url = urljoin(base_url, link['href'])
            if full_url not in self.visited and full_url not in self.to_visit:
                self.to_visit.append(full_url)

if __name__ == "__main__":
    start_url = "http://example.com"  # Başlangıç URL'si
    max_pages = 10  # Taramak istediğiniz maksimum sayfa sayısı
    spider = SimpleSpider(start_url, max_pages)
    spider.crawl()
