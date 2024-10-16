import requests
import json
import time
import argparse
from datetime import datetime

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
    parser = argparse.ArgumentParser(description="Nessus taraması başlatma scripti")
    parser.add_argument('nessus_url', type=str, help='Nessus sunucusunun URL adresi')
    parser.add_argument('username', type=str, help='Nessus kullanıcı adı')
    parser.add_argument('password', type=str, help='Nessus şifresi')
    parser.add_argument('host_file', type=str, help='Tarama yapılacak hostların bulunduğu dosya yolu')
    parser.add_argument('--policy_id', type=str, help='Opsiyonel olarak kullanılacak policy ID', default=None)

    args = parser.parse_args()

    # Nessus sunucusuna giriş yap
    token = login(args.nessus_url, args.username, args.password)

    # Host dosyasını oku
    with open(args.host_file, 'r') as f:
        hosts = [line.strip() for line in f.readlines()]

    # Scan başlat
    scan_name = f"Tarama {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    start_scan(args.nessus_url, token, scan_name, args.policy_id, hosts)
    time.sleep(1)  # Sunucuya aşırı yüklenmemek için küçük bir bekleme

if __name__ == '__main__':
    main()
