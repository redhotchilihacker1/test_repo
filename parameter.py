import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
from collections import deque

def find_urls_with_params(base_url, depth):
    visited = set()  # Ziyaret edilen URL'leri saklamak için
    urls_with_params = []  # Parametre barındıran URL'ler için liste
    queue = deque([(base_url, 0)])  # URL ve derinlik için deque

    while queue:
        current_url, current_depth = queue.popleft()
        
        if current_depth > depth:
            continue
        
        if current_url in visited:
            continue

        visited.add(current_url)
        
        try:
            response = requests.get(current_url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error fetching {current_url}: {e}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        # Linkleri bul
        for link in soup.find_all('a', href=True):
            full_url = urljoin(current_url, link['href'])
            parsed_url = urlparse(full_url)
            query_params = parse_qs(parsed_url.query)

            if query_params:
                urls_with_params.append(full_url)
                print(f"Found parameterized URL: {full_url}")

            # Derinliği kontrol et ve kuyruğa ekle
            if current_depth < depth:
                queue.append((full_url, current_depth + 1))

    return urls_with_params

def main():
    base_url = input("URL girin: ")
    depth = int(input("Tarama derinliği girin: "))
    
    urls = find_urls_with_params(base_url, depth)
    
    print("\nParametre barındıran toplam URL sayısı:", len(urls))
    if urls:
        print("Parametre barındıran URL'ler:")
        for url in urls:
            print(url)
    else:
        print("Parametre barındıran URL bulunamadı.")

if __name__ == "__main__":
    main()
