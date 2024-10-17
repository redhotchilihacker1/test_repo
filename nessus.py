import requests
import json

def start_scan(base_url, access_key, secret_key, scan_name, targets, policy_name):
    headers = {
        'X-ApiKeys': f'accessKey={access_key}; secretKey={secret_key}',
        'Content-Type': 'application/json'
    }

    # Politika UUID'sini ad ile bul
    policy_uuid = get_policy_uuid_by_name(base_url, headers, policy_name)

    # Tarama ayarlarını oluştur
    scan_settings = {
        "uuid": policy_uuid,
        "settings": {
            "name": scan_name,
            "text_targets": targets,
            "enabled": True
        }
    }

    # Tarama oluştur
    response = requests.post(f"{base_url}/scans", headers=headers, json=scan_settings, verify=False)
    
    if response.status_code != 200:
        print(f"Tarama oluşturulamadı. Hata kodu: {response.status_code}. Detay: {response.json()}")
        return

    scan_id = response.json()['scan']['id']
    print(f"Tarama başlatıldı. Tarama ID: {scan_id}")

def get_policy_uuid_by_name(base_url, headers, policy_name):
    # Politika listelerini Nessus'tan çekiyoruz
    response = requests.get(f"{base_url}/policies", headers=headers, verify=False)
    
    if response.status_code != 200:
        raise Exception(f"Politikalar alınırken hata oluştu: {response.text}")

    policies = response.json()
    
    # Politika listesinde anahtarların mevcut olup olmadığını kontrol et
    if 'policies' not in policies:
        raise KeyError("Politika verisi bulunamadı.")

    # Politika adını kullanarak UUID'yi bul
    for policy in policies['policies']:
        if 'uuid' not in policy:
            raise KeyError(f"Politika '{policy['name']}' için UUID bulunamadı.")
        if policy['name'] == policy_name:  # Politika adını kontrol et
            return policy['uuid']
    
    raise KeyError("Verilen politika adı için UUID bulunamadı.")
    print(policies)

if __name__ == "__main__":
    # Kullanıcıdan gerekli bilgiler alınıyor
    base_url = "https://<nessus_server_ip>:8834"  # Nessus sunucunun IP adresini buraya yaz
    access_key = input("Access Key: ")
    secret_key = input("Secret Key: ")
    scan_name = input("Tarama adı: ")
    targets = input("Hedefler (IP adresleri, virgülle ayrılmış): ")
    policy_name = input("Politika adı: ")  # Policy ID yerine politika adı alınıyor

    start_scan(base_url, access_key, secret_key, scan_name, targets, policy_name)
