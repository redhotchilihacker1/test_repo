import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs

def find_urls_with_params(base_url):
    try:
        response = requests.get(base_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {base_url}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    urls_with_params = []

    for link in soup.find_all('a', href=True):
        full_url = urljoin(base_url, link['href'])
        parsed_url = urlparse(full_url)
        query_params = parse_qs(parsed_url.query)

        if query_params:
            urls_with_params.append(full_url)

    return urls_with_params

def main():
    base_url = input("URL girin: ")
    urls = find_urls_with_params(base_url)
    
    if urls:
        print("Parametre barındıran URL'ler:")
        for url in urls:
            print(url)
    else:
        print("Parametre barındıran URL bulunamadı.")

if __name__ == "__main__":
    main()
