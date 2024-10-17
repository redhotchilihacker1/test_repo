import requests
import os
import subprocess

# Nessus API bilgileri
nessus_url = "https://<nessus_server_address>:8834"
api_key = "<your_api_key>"
secret_key = "<your_secret_key>"

# Nessus API'ye bağlantı için gereken başlıklar
headers = {
    'X-ApiKeys': f'accessKey={api_key}; secretKey={secret_key}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def download_nessus_file(scan_id, output_filename):
    # Nessus API endpoint: .nessus dosyasını indirmek için
    download_url = f"{nessus_url}/scans/{scan_id}/export?format=nessus"

    # Export başlat
    response = requests.post(download_url, headers=headers, verify=False)
    if response.status_code == 200:
        file_token = response.json()["file"]
        # Export edilmiş dosyayı indir
        file_download_url = f"{nessus_url}/scans/{scan_id}/export/{file_token}/download"
        response = requests.get(file_download_url, headers=headers, verify=False)

        if response.status_code == 200:
            # Dosyayı kaydet
            with open(output_filename, "wb") as file:
                file.write(response.content)
            print(f"{output_filename} başarıyla indirildi.")
        else:
            print("Dosya indirilemedi.")
            return False
    else:
        print("Export başlatılamadı.")
        return False
    return True

def run_existing_script(nessus_file, output_name):
    # Hali hazırda olan scripti çalıştır
    try:
        subprocess.run(["python3", "benim_script.py", nessus_file, output_name], check=True)
        print("Script başarıyla çalıştırıldı.")
    except subprocess.CalledProcessError as e:
        print(f"Script çalıştırma sırasında hata oluştu: {e}")

if __name__ == "__main__":
    # Kullanıcıdan scan_id girişi al
    scan_id = input("Scan ID'yi girin: ")
    
    # Kullanıcıdan dosya adı girişi al
    output_name = input("Çıktı dosyasının adını girin (uzantısız): ")

    # İndirilecek olan .nessus dosyasının adı
    output_filename = "scan_result.nessus"

    if download_nessus_file(scan_id, output_filename):
        # Scripti çağır
        run_existing_script(output_filename, output_name)
