import requests
import json
import argparse

# Nessus'a giriş fonksiyonu
def nessus_login(nessus_url, username, password):
    login_url = f"{nessus_url}/session"
    
    headers = {"Content-Type": "application/json"}
    login_data = {
        "username": username,
        "password": password
    }

    response = requests.post(login_url, headers=headers, data=json.dumps(login_data), verify=False)

    if response.status_code == 200:
        token = response.json()["token"]
        print(f"Giriş başarılı. Token: {token}")
        return token
    else:
        print(f"Giriş başarısız. Hata: {response.status_code}")
        return None

# Tarama başlatma fonksiyonu
def start_scan(nessus_url, token, scan_name, targets, policy_id=None):
    headers = {
        "Content-Type": "application/json",
        "X-Cookie": f"token={token}"
    }

    # Eğer politika verilmemişse varsayılan politikayı kullan
    if policy_id is None:
        policies_url = f"{nessus_url}/policies"
        response = requests.get(policies_url, headers=headers, verify=False)
        if response.status_code == 200:
            policies = response.json()['policies']
            if policies:
                policy_id = policies[0]['uuid']  # İlk politikayı alıyoruz
                print(f"Politika belirtilmedi, varsayılan politika kullanılıyor: {policy_id}")
            else:
                print("Hiçbir politika bulunamadı!")
                return
        else:
            print(f"Politika listesi alınamadı. Hata kodu: {response.status_code}")
            return

    # Tarama verilerini oluştur
    scan_data = {
        "uuid": policy_id,
        "settings": {
            "name": scan_name,
            "enabled": True,
            "text_targets": targets
        }
    }

    # Tarama oluşturma isteği
    create_scan_url = f"{nessus_url}/scans"
    response = requests.post(create_scan_url, headers=headers, data=json.dumps(scan_data), verify=False)

    if response.status_code == 200:
        scan_id = response.json()['scan']['id']
        print(f"Tarama oluşturuldu. Tarama ID: {scan_id}")

        # Tarama başlatma
        launch_scan_url = f"{nessus_url}/scans/{scan_id}/launch"
        launch_response = requests.post(launch_scan_url, headers=headers, verify=False)

        if launch_response.status_code == 200:
            print(f"Tarama başlatıldı: {scan_name}")
        else:
            print(f"Tarama başlatılamadı. Hata kodu: {launch_response.status_code}")
    else:
        print(f"Tarama oluşturulamadı. Hata kodu: {response.status_code}")

# Nessus sunucusu ile bağlantı kurma fonksiyonu
def connect_to_nessus(nessus_url, token):
    headers = {
        "Content-Type": "application/json",
        "X-Cookie": f"token={token}"
    }

    version_url = f"{nessus_url}/server/properties"
    response = requests.get(version_url, headers=headers, verify=False)

    if response.status_code == 200:
        print("Sunucu bilgileri:")
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Sunucuya bağlanırken bir hata oluştu. Hata kodu: {response.status_code}")

# Argümanlar için komut satırı arayüzü
def main():
    parser = argparse.ArgumentParser(description="Nessus sunucusuna bağlan ve tarama başlat.")
    parser.add_argument("-u", "--url", required=True, help="Nessus sunucu URL'si (örneğin: https://<nessus_server>:8834)")
    parser.add_argument("-n", "--username", required=True, help="Nessus kullanıcı adı")
    parser.add_argument("-p", "--password", required=True, help="Nessus şifresi")
    parser.add_argument("-f", "--hosts_file", required=True, help="Hedef hostların bulunduğu dosya")
    parser.add_argument("-s", "--scan_name", required=True, help="Başlatılacak taramanın adı")
    parser.add_argument("-i", "--policy_id", required=False, help="Tarama politikası UUID (opsiyonel)")

    args = parser.parse_args()

    # Hedef hostları dosyadan oku
    with open(args.hosts_file, 'r') as file:
        targets = file.read().replace("\n", ",")

    # Giriş yap ve token al
    token = nessus_login(args.url, args.username, args.password)

    # Eğer token alındıysa tarama başlat
    if token:
        connect_to_nessus(args.url, token)
        start_scan(args.url, token, args.scan_name, targets, args.policy_id)

if __name__ == "__main__":
    main()
