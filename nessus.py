import requests
import json

# Nessus API bilgileri
nessus_url = 'https://<Nessus_Server_IP>:8834'
api_key = '<Your_API_Key>'
secret_key = '<Your_Secret_Key>'

# Tarama politikası ve hedef dosyası
policy_id = '<Policy_ID>'  # Tarama politikası ID'si
target_file = 'targets.txt'  # Hedeflerin bulunduğu dosya

# Nessus API'sine bağlanma ve kimlik doğrulama
def authenticate():
    headers = {
        'X-ApiKeys': f'accessKey={api_key}; secretKey={secret_key}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(f'{nessus_url}/session', headers=headers, verify=False)
    if response.status_code == 200:
        print('Başarıyla kimlik doğrulandı.')
        return headers
    else:
        print('Kimlik doğrulama hatası:', response.content)
        return None

# Tarama başlatma fonksiyonu
def start_scan(headers, policy_id, targets):
    # Tarama oluşturma
    scan_data = {
        'uuid': policy_id,
        'settings': {
            'name': 'Automated Scan',
            'policy_id': policy_id,
            'text_targets': targets
        }
    }
    
    response = requests.post(f'{nessus_url}/scans', headers=headers, json=scan_data, verify=False)
    
    if response.status_code == 200:
        scan_id = response.json()['scan']['id']
        print(f'Tarama başarıyla başlatıldı. Tarama ID: {scan_id}')
    else:
        print('Tarama başlatma hatası:', response.content)

# Ana program
def main():
    headers = authenticate()
    if headers:
        # Hedef dosyasını oku
        with open(target_file, 'r') as f:
            targets = f.read().strip()
        
        start_scan(headers, policy_id, targets)

if __name__ == '__main__':
    main()
