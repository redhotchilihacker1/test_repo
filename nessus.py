import argparse
import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# HTTPS sertifika uyarılarını devre dışı bırak
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def get_policy_uuid(base_url, headers, policy_id):
    # Nessus'tan politika listesini al
    response = requests.get(f"{base_url}/policies", headers=headers, verify=False)
    
    if response.status_code == 200:
        policies = response.json()
        print("Policies JSON:", json.dumps(policies, indent=2))  # Gelen JSON'u yazdır
        
        # Gelen politikalarda istenen policy_id'yi bul ve uuid'yi döndür
        for policy in policies.get('policies', []):
            if policy['id'] == policy_id:
                return policy.get('uuid') or policy.get('template_uuid')  # uuid veya template_uuid'yi kontrol et
        
        raise KeyError("Policy UUID not found for the given policy_id.")
    else:
        print(f"Failed to retrieve policies: {response.status_code}")
        return None

def start_scan(base_url, access_key, secret_key, scan_name, targets, policy_id=None):
    headers = {
        "X-ApiKeys": f"accessKey={access_key}; secretKey={secret_key}",
        "Content-Type": "application/json"
    }
    
    # Eğer policy_id verilmişse, UUID'sini alalım
    if policy_id:
        policy_uuid = get_policy_uuid(base_url, headers, policy_id)
    else:
        policy_uuid = None
    
    # Tarama ayarlarını yapılandır
    scan_settings = {
        "uuid": policy_uuid,
        "settings": {
            "name": scan_name,
            "text_targets": targets
        }
    }
    
    # Tarama isteğini gönder
    response = requests.post(f"{base_url}/scans", headers=headers, json=scan_settings, verify=False)
    
    if response.status_code == 200:
        scan = response.json()
        print(f"Tarama başarıyla oluşturuldu! Scan ID: {scan['scan']['id']}")
    else:
        print(f"Tarama oluşturulamadı. Hata kodu: {response.status_code}")
        print("Detaylı hata mesajı:", response.json())

def main():
    parser = argparse.ArgumentParser(description="Nessus tarama başlatma scripti.")
    parser.add_argument("--url", required=True, help="Nessus sunucusunun URL'si. Örnek: https://nessus.local:8834")
    parser.add_argument("--api_key", required=True, help="Nessus API Access Key")
    parser.add_argument("--secret_key", required=True, help="Nessus API Secret Key")
    parser.add_argument("--scan_name", required=True, help="Oluşturulacak taramanın adı")
    parser.add_argument("--targets", required=True, help="Tarama yapılacak hedeflerin listesi (IP veya domain)")
    parser.add_argument("--policy_id", required=False, help="Opsiyonel: Taramada kullanılacak policy ID")

    args = parser.parse_args()

    start_scan(args.url, args.api_key, args.secret_key, args.scan_name, args.targets, args.policy_id)

if __name__ == "__main__":
    main()
