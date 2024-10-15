import socket
import requests
import time
import argparse

# Argümanları al
parser = argparse.ArgumentParser(description="Reverse proxy arkasındaki origin host'u tespit et.")
parser.add_argument("url", help="Tespit edilecek URL (örneğin: http://example.com)")
args = parser.parse_args()

# Kullanıcının girdiği URL
target_url = args.url

# DNS çözümleme
def dns_lookup(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

# HTTP header'larını kontrol et
def check_http_headers(url):
    try:
        response = requests.get(url)
        headers = response.headers
        print("HTTP Headers:")
        for header, value in headers.items():
            print(f"{header}: {value}")
    except requests.RequestException as e:
        print(f"HTTP isteği başarısız oldu: {e}")

# Timing attack
def timing_attack(url):
    try:
        times = []
        for _ in range(5):
            start_time = time.time()
            requests.get(url)
            response_time = time.time() - start_time
            times.append(response_time)
            print(f"Yanıt süresi: {response_time:.4f} saniye")
        avg_time = sum(times) / len(times)
        print(f"Ortalama yanıt süresi: {avg_time:.4f} saniye")
    except requests.RequestException as e:
        print(f"HTTP isteği başarısız oldu: {e}")

# DNS çözümlemesi ile başlayalım
origin_ip = dns_lookup(target_url.replace("http://", "").replace("https://", "").split("/")[0])
if origin_ip:
    print(f"DNS çözümlemesi sonucu IP adresi: {origin_ip}")
else:
    print("DNS çözümlemesi yapılamadı.")

# HTTP header'larını kontrol et
check_http_headers(target_url)

# Timing attack denemesi
print("\nTiming attack denemesi yapılıyor...")
timing_attack(target_url)
