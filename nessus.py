import requests
import json
import argparse

# Nessus'a giriş fonksiyonu
def nessus_login(nessus_url, username, password):
    # Nessus API login endpoint'i
    login_url = f"{nessus_url}/session"
    
    headers = {"Content-Type": "application/json"}
    login_data = {
        "username": username,
        "password": password
    }

    # Nessus'a giriş isteği
    response = requests.post(login_url, headers=headers, data=json.dumps(login_data), verify=False)

    # Giriş başarılıysa token döner
    if response.status_code == 200:
        token = response.json()["token"]
        print(f"Giriş başarılı. Token: {token}")
        return token
    else:
        print(f"Giriş başarısız. Hata: {response.status_code}")
        return None

# Nessus sunucusu ile bağlantı kurma fonksiyonu
def connect_to_nessus(nessus_url, token):
    headers = {
        "Content-Type": "application/json",
        "X-Cookie": f"token={token}"
    }
    
    # Sunucu özelliklerini al
    version_url = f"{nessus_url}/server/properties"
    response = requests.get(version_url, headers=headers, verify=False)

    # Eğer başarılıysa sunucu bilgilerini yazdır
    if response.status_code == 200:
        print("Sunucu bilgileri:")
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Sunucuya bağlanırken bir hata oluştu. Hata kodu: {response.status_code}")

# Argümanlar için komut satırı arayüzü
def main():
    # Argümanları ayarla
    parser = argparse.ArgumentParser(description="Nessus sunucusuna bağlan ve login ol.")
    parser.add_argument("-u", "--url", required=True, help="Nessus sunucu URL'si (örneğin: https://<nessus_server>:8834)")
    parser.add_argument("-n", "--username", required=True, help="Nessus kullanıcı adı")
    parser.add_argument("-p", "--password", required=True, help="Nessus şifresi")
    
    args = parser.parse_args()

    # Giriş yap ve token al
    token = nessus_login(args.url, args.username, args.password)

    # Eğer token alındıysa sunucuya bağlan
    if token:
        connect_to_nessus(args.url, token)

if __name__ == "__main__":
    main()
