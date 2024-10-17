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

def get_policy_uuid(base_url, headers, policy_id):
    # Politika listelerini Nessus'tan çekiyoruz
    response = requests.get(f"{base_url}/policies", headers=headers, verify=False)
    policies = response.json()

    # Tüm politikalar içinde istenen policy_id'yi bul ve uuid'yi döndür
    for policy in policies.get('policies', []):
        if policy['id'] == policy_id:
            return policy.get('uuid') or policy.get('template_uuid')  # 'uuid' yoksa 'template_uuid'yi kullan
    raise KeyError("Policy UUID not found for the given policy_id.")

if __name__ == "__main__":
    # Kullanıcıdan gerekli bilgiler alınıyor
    base_url = "https://<nessus_server_ip>:8834"
    access_key = input("Access Key: ")
    secret_key = input("Secret Key: ")
    scan_name = input("Tarama adı: ")
    targets = input("Hedefler (IP adresleri, virgülle ayrılmış): ")
    policy_id = input("Policy ID (opsiyonel): ") or None

    start_scan(base_url, access_key, secret_key, scan_name, targets, policy_id)
