from tenable.io import TenableIO
import argparse

# Tarama başlatma fonksiyonu
def start_scan(nessus_url, api_key, secret_key, scan_name, targets, policy_id=None):
    # Tenable.io nesnesi oluştur
    tio = TenableIO(api_key, secret_key)

    # Tarama politikalarını al
    if policy_id is None:
        policies = tio.policies.list()
        if policies:
            policy_id = policies[0]['id']  # İlk politikayı alıyoruz
            print(f"Politika belirtilmedi, varsayılan politika kullanılıyor: {policy_id}")
        else:
            print("Hiçbir politika bulunamadı!")
            return

    # Tarama ayarlarını oluştur
    scan_settings = {
        'uuid': policy_id,
        'settings': {
            'name': scan_name,
            'enabled': True,
            'text_targets': targets
        }
    }

    # Tarama oluşturma
    scan = tio.scans.create(scan_settings)
    print(f"Tarama oluşturuldu. Tarama ID: {scan['id']}")

    # Tarama başlatma
    tio.scans.launch(scan['id'])
    print(f"Tarama başlatıldı: {scan_name}")

# Argümanlar için komut satırı arayüzü
def main():
    parser = argparse.ArgumentParser(description="Nessus sunucusuna bağlan ve tarama başlat.")
    parser.add_argument("-u", "--url", required=True, help="Nessus sunucu URL'si (örneğin: https://<nessus_server>:8834)")
    parser.add_argument("-k", "--api_key", required=True, help="Nessus API anahtarı")
    parser.add_argument("-s", "--secret_key", required=True, help="Nessus gizli anahtarı")
    parser.add_argument("-f", "--hosts_file", required=True, help="Hedef hostların bulunduğu dosya")
    parser.add_argument("-n", "--scan_name", required=True, help="Başlatılacak taramanın adı")
    parser.add_argument("-i", "--policy_id", required=False, help="Tarama politikası ID (opsiyonel)")

    args = parser.parse_args()

    # Hedef hostları dosyadan oku
    with open(args.hosts_file, 'r') as file:
        targets = file.read().replace("\n", ",")  # Hedefleri virgülle ayır

    # Tarama başlat
    start_scan(args.url, args.api_key, args.secret_key, args.scan_name, targets, args.policy_id)

if __name__ == "__main__":
    main()
