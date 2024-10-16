import requests
import json
import time
from datetime import datetime

# Nessus sunucusu bilgileri
nessus_servers = [
    {
        'url': 'https://<nessus_server1>:8834',
        'username': '<username>',
        'password': '<password>'
    },
    {
        'url': 'https://<nessus_server2>:8834',
        'username': '<username>',
        'password': '<password>'
    }
]

# Nessus API'ye login olma fonksiyonu
def login(nessus_url, username, password):
    login_url = f"{nessus_url}/session"
    data = {'username': username, 'password': password}
    response = requests.post(login_url, data=json.dumps(data), headers={'Content-Type': 'application/json'}, verify=False)
    return response.json()['token']

# Tarama başlatma fonksiyonu
def start_scan(nessus_url, token, scan_name, policy_id=None, hosts=[]):
    headers = {'X-Cookie': f'token={token}', 'Content-Type': 'application/json'}
    scan_data = {
        "uuid": policy_id if policy_id else "template-uuid",
        "settings": {
            "name": scan_name,
            "text_targets": ','.join(hosts),
            "launch_now": True
        }
    }

    response = requests.post(f"{nessus_url}/scans", headers=headers, data=json.dumps(scan_data), verify=False)
    if response.status_code == 200:
        print(f"Tarama başlatıldı: {scan_name}")
    else:
        print(f"Hata oluştu: {response.text}")

# Ana fonksiyon
def main():
    for server in nessus_servers:
        token = login(server['url'], server['username'], server['password'])
        
        # Host dosyasını oku
        with open('<path_to_host_file>', 'r') as f:
            hosts = [line.strip() for line in f.readlines()]

        # Policy opsiyonel, varsa ID'sini ekleyin
        policy_id = None  # Eğer spesifik bir policy kullanılacaksa buraya ID eklenmeli

        # Scan başlat
        scan_name = f"Tarama {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        start_scan(server['url'], token, scan_name, policy_id, hosts)
        time.sleep(1)  # Sunucuya aşırı yüklenmemek için küçük bir bekleme

if __name__ == '__main__':
    main()
