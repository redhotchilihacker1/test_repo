import requests
import json
import argparse
from datetime import datetime
import urllib3

# InsecureRequestWarning uyarısını devre dışı bırak (SSL doğrulaması kapalıysa)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Nessus API'ye login olma fonksiyonu
def login(nessus_url, username, password, verify_ssl):
    login_url = f"{nessus_url}/session"
    data = {'username': username, 'password': password}
    response = requests.post(login_url, data=json.dumps(data), headers={'Content-Type': 'application/json'}, verify=verify_ssl)
    return response.json()['token']

# Tarama başlatma fonksiyonu
def start_scan(nessus_url, token, scan_name, hosts, policy_id=None, verify_ssl=True):
    headers = {'X-Cookie': f'token={token}', 'Content-Type': 'application/json'}
    scan_data = {
        "uuid": policy_id if policy_id else "template-uuid",
        "settings": {
            "name": scan_name,
            "text_targets": ','.join(hosts),
            "launch_now": True
        }
    }

    response = requests.post(f"{nessus_url}/scans", headers=headers, data=json.dumps(scan_data), verify=verify_ssl)
    if response.status_code == 200:
        print(f"Tarama başlatıldı: {scan_name}")
    else:
        print(f"Hata oluştu: {response.text}")

# Ana fonksiyon
def main(nessus_url, username, password, host_file, policy_id=None, verify_ssl=True):
    token = login(nessus_url, username, password, verify_ssl)
    
    # Host dosyasını oku
    with open(host_file, 'r') as f:
        hosts = [line.strip() for line in f.readlines()]

    # Scan başlat
    scan_name = f"Tarama {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    start_scan(nessus_url, token, scan_name, hosts, policy_id, verify_ssl)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Nessus tarama scripti")
    parser.add_argument('--nessus_url', required=True, help="Nessus sunucusu URL'si (örnek: https://<nessus_server>:8834)")
    parser.add_argument('--username', required=True, help="Nessus kullanıcı adı")
    parser.add_argument('--password', required=True, help="Nessus şifresi")
    parser.add_argument('--host_file', required=True, help="Tarama yapılacak host dosyasının yolu")
    parser.add_argument('--policy_id', help="Kullanılacak policy ID (opsiyonel)", default=None)
    parser.add_argument('--verify_ssl', action='store_true', help="SSL doğrulaması yapılsın mı? (varsayılan: yapılmaz)", default=False)
    
    args = parser.parse_args()

    main(args.nessus_url, args.username, args.password, args.host_file, args.policy_id, args.verify_ssl)
