import xml.etree.ElementTree as ET
import pandas as pd
import sys
import re

# Kullanıcıdan dosya yolunu ve kaydedilecek dosya adını al
if len(sys.argv) != 3:
    print("Kullanım: python script.py <input.nessus> <output_filename>")
    sys.exit(1)

nessus_file = sys.argv[1]
output_filename = sys.argv[2]

# XML dosyasını temizleme
with open(nessus_file, 'r', encoding='utf-8') as file:
    xml_content = file.read()
    # Hatalı HTML etiketlerini temizle
    clean_content = re.sub(r'<[^>]*>', lambda m: m.group(0) if m.group(0).startswith('<![CDATA[') else '', xml_content)

# Nessus dosyasını XML olarak yükle
root = ET.fromstring(clean_content)

# Verileri tutmak için listeler
data = []

# Nessus dosyasındaki her host'u işle
for report_host in root.findall(".//ReportHost"):
    dns_name = report_host.attrib.get('name')
    ip_address = None
    
    for tag in report_host.findall("HostProperties/tag"):
        if tag.attrib.get('name') == 'host-ip':
            ip_address = tag.text
    
    # Her host'un zafiyetlerini bul
    for report_item in report_host.findall("ReportItem"):
        plugin_name = report_item.attrib.get('pluginName', 'N/A')
        synopsis = report_item.findtext('synopsis', 'N/A')
        description = report_item.findtext('description', 'N/A')
        see_also = report_item.findtext('see_also', 'N/A')
        solution = report_item.findtext('solution', 'N/A')
        risk_factor = report_item.findtext('risk_factor', 'N/A')
        
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
