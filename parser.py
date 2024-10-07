import csv
from bs4 import BeautifulSoup

# HTML dosyasının yolunu belirtin
input_html_file = 'path_to_your_nessus_report.html'
output_csv_file = 'vulnerabilities_report.csv'

# HTML dosyasını okuyun
with open(input_html_file, 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

# CSV dosyasını yazma için hazırlayın
with open(output_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Bulgu Başlığı', 'IP Adresi:Portu', 'Risk Faktörü', 'CVSS Skoru']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # CSV başlıklarını yaz
    writer.writeheader()

    # Zafiyetleri bulma
    for vuln in soup.find_all('tr', class_='vulnerability'):
        title = vuln.find('td', class_='title').text.strip()
        ip_port = vuln.find('td', class_='ip-port').text.strip()
        risk_factor = vuln.find('td', class_='risk-factor').text.strip()
        cvss_score = vuln.find('td', class_='cvss').text.strip()

        # CSV'ye yaz
        writer.writerow({
            'Bulgu Başlığı': title,
            'IP Adresi:Portu': ip_port,
            'Risk Faktörü': risk_factor,
            'CVSS Skoru': cvss_score
        })

print(f'Rapor başarıyla {output_csv_file} dosyasına yazıldı.')
