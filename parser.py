import xml.etree.ElementTree as ET
import pandas as pd
from bs4 import BeautifulSoup
import sys

# Kullanıcıdan dosya yolunu ve kaydedilecek dosya adını al
if len(sys.argv) != 3:
    print("Kullanım: python script.py <input.nessus> <output_filename>")
    sys.exit(1)

nessus_file = sys.argv[1]
output_filename = sys.argv[2]

# Nessus dosyasını yükle ve BeautifulSoup ile ayrıştır
with open(nessus_file, 'r', encoding='utf-8') as file:
    content = file.read()
    soup = BeautifulSoup(content, 'xml')  # XML olarak ayrıştır

# Verileri tutmak için listeler
data = []

# Nessus dosyasındaki her host'u işle
for report_host in soup.find_all("ReportHost"):
    dns_name = report_host.get('name')
    ip_address = None
    
    for tag in report_host.find_all("tag"):
        if tag.get('name') == 'host-ip':
            ip_address = tag.text
    
    # Her host'un zafiyetlerini bul
    for report_item in report_host.find_all("ReportItem"):
        plugin_name = report_item.get('pluginName', 'N/A')
        synopsis = report_item.find('synopsis').text if report_item.find('synopsis') else 'N/A'
        description = report_item.find('description').text if report_item.find('description') else 'N/A'
        see_also = report_item.find('see_also').text if report_item.find('see_also') else 'N/A'
        solution = report_item.find('solution').text if report_item.find('solution') else 'N/A'
        risk_factor = report_item.find('risk_factor').text if report_item.find('risk_factor') else 'N/A'
        
        # Verileri bir satır olarak kaydet
        data.append({
            'DNS Name': dns_name,
            'IP': ip_address,
            'Vulnerability': plugin_name,
            'Synopsis': synopsis,
            'Description': description,
            'References': see_also,
            'Solution': solution,
            'Risk Factor': risk_factor
        })

# Verileri pandas DataFrame'e dönüştür
df = pd.DataFrame(data)

# CSV olarak kaydet
csv_output = f'{output_filename}.csv'
df.to_csv(csv_output, index=False)

# XLSX olarak kaydet
xlsx_output = f'{output_filename}.xlsx'
df.to_excel(xlsx_output, index=False)

print(f"CSV kaydedildi: {csv_output}")
print(f"XLSX kaydedildi: {xlsx_output}")
