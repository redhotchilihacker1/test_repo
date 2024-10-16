import requests
import json
import argparse
from datetime import datetime
import urllib3

# InsecureRequestWarning uyarısını devre dışı bırak
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
