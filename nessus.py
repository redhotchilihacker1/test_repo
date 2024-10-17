import requests
import json

def start_scan(base_url, access_key, secret_key, scan_name, targets, policy_id=None):
    # Nessus'a bağlanırken kimlik doğrulaması için gerekli header'lar
    headers = {
        'X-ApiKeys': f'accessKey={access_key}; secretKey={secret_key}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    # Tarama için gerekli ayarları yapılandırma
    scan_settings = {
        "uuid": get_policy_uuid(base_url, headers, policy_id),  # Policy UUID alınıyor
        "settings": {
            "name": scan_name,
            "text_targets": targets
        }
    }

    # Tarama başlatma isteği
    response = requests.post(f'{base_url}/scans', headers=headers, json=scan_settings, verify=False)

    if response.status_code == 200:
        scan_id = response.json()['scan']['id']
        print(f'Tarama başarıyla oluşturuldu. Tarama ID: {scan_id}')
    else:
        print(f'Tarama oluşturulamadı. Hata kodu: {response.status_code}')
        print(f'Hata mesajı: {response.text}')

def get_policy_uuid(base_url, headers, policy_id=None):
    # Policy UUID almak için istek
    response = requests.get(f'{base_url}/policies', headers=headers, verify=False)

    if response.status_code == 200:
        policies = response.json()['policies']
        for policy in policies:
            if policy_id and policy['id'] == policy_id:
                return policy['uuid']  # Eğer policy ID verilmişse ona göre UUID döndür
        # Eğer policy ID verilmemişse varsayılan policy UUID döndür
        return policies[0]['uuid']
    else:
        print(f'Policy UUID alınamadı. Hata kodu: {response.status_code}')
        return None

if __name__ == "__main__":
    # Kullanıcıdan gerekli bilgiler alınıyor
    base_url = "https://<nessus_server_ip>:8834"
    access_key = input("Access Key: ")
    secret_key = input("Secret Key: ")
    scan_name = input("Tarama adı: ")
    targets = input("Hedefler (IP adresleri, virgülle ayrılmış): ")
    policy_id = input("Policy ID (opsiyonel): ") or None

    start_scan(base_url, access_key, secret_key, scan_name, targets, policy_id)
