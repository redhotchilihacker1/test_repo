import os
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm  # Progress bar için

# Nessus dosyalarının bulunduğu klasördeki tüm .nessus dosyalarını bul
nessus_files = [f for f in os.listdir('.') if f.endswith('.nessus')]

# Verileri tutmak için listeler
all_data = []

# Risk Factor önceliklerini tanımla
risk_order = {
    "Critical": 1,
    "High": 2,
    "Medium": 3,
    "Low": 4,
    "None": 5  # "None" olanları en sona eklemek için
}

# Her .nessus dosyasını işle
for nessus_file in nessus_files:
    # Her dosya için ayrı bir progress bar
    with tqdm(total=1, desc=f"Processing {nessus_file}", unit="file") as pbar:
        # Nessus dosyasını yükle ve BeautifulSoup ile ayrıştır
        with open(nessus_file, 'r', encoding='utf-8') as file:
            content = file.read()
            soup = BeautifulSoup(content, 'xml')  # XML olarak ayrıştır
        
        # Verileri tutmak için liste
        data = []

        # Nessus dosyasındaki tüm hostları işle
        report_hosts = soup.find_all("ReportHost")
        for report_host in report_hosts:
            dns_name = report_host.get('name')
            ip_address = None
            
            for tag in report_host.find_all("tag"):
                if tag.get('name') == 'host-ip':
                    ip_address = tag.text
            
            # Host'un zafiyetlerini bul
            report_items = report_host.find_all("ReportItem")
            for report_item in report_items:
                plugin_name = report_item.get('pluginName', 'N/A')
                synopsis = report_item.find('synopsis').text if report_item.find('synopsis') else 'N/A'
                description = report_item.find('description').text if report_item.find('description') else 'N/A'
                see_also = report_item.find('see_also').text if report_item.find('see_also') else 'N/A'
                solution = report_item.find('solution').text if report_item.find('solution') else 'N/A'
                risk_factor = report_item.find('risk_factor').text if report_item.find('risk_factor') else 'N/A'
                
                # Risk Factor "None" ise bu satırı atla
                if risk_factor == "None":
                    continue
                
                # Port/Service/Protocol değerlerini al
                port = report_item.get('port', 'N/A')
                svc_name = report_item.get('svc_name', 'N/A')
                protocol = report_item.get('protocol', 'N/A')
                
                # Port 0 ise N/A olarak ayarla
                if port == '0':
                    port = 'N/A'
                
                # Birleştir ve formata uygun hale getir
                port_service_protocol = f"{port}/{svc_name}/{protocol}"
                
                # CVSS değerini al
                cvss_vector = report_item.find('cvss_vector').text if report_item.find('cvss_vector') else 'N/A'
                
                # Verileri bir satır olarak kaydet
                data.append({
                    'DNS Name': dns_name,
                    'IP': ip_address,
                    'Risk Factor': risk_factor,
                    'Vulnerability': plugin_name,
                    'Port/Service/Protocol': port_service_protocol,
                    'CVSS': cvss_vector,
                    'Synopsis': synopsis,
                    'Description': description,
                    'References': see_also,
                    'Solution': solution
                })
        
        # Verileri pandas DataFrame'e dönüştür ve Risk Factor'e göre sırala
        df = pd.DataFrame(data)
        df['Risk Factor Order'] = df['Risk Factor'].map(risk_order)
        df = df.sort_values(by='Risk Factor Order').drop(columns='Risk Factor Order')
        
        # Başlık sırasını koru
        df = df[['DNS Name', 'IP', 'Risk Factor', 'Vulnerability', 'Port/Service/Protocol', 'CVSS', 'Synopsis', 'Description', 'References', 'Solution']]
        
        # Her dosyadan elde edilen sonuçları genel listeye ekle, ardından bir boş satır ekle
        all_data.append(df)
        all_data.append(pd.DataFrame([[""] * len(df.columns)], columns=df.columns))  # Boş satır
        
        # İlerleme çubuğunu tamamla
        pbar.update(1)

# Tüm verileri tek bir DataFrame'de birleştir
final_df = pd.concat(all_data, ignore_index=True)

# XLSX olarak kaydet
xlsx_output = 'output_data.xlsx'
final_df.to_excel(xlsx_output, index=False)

print(f"XLSX kaydedildi: {xlsx_output}")
