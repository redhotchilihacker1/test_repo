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
    vulnerabilities_found = False
    for row in soup.find_all('tr'):
        columns = row.find_all('td')
        
        if len(columns) >= 4:  # Eğer yeterli sütun varsa
            title = columns[0].get_text(strip=True)
            ip_port = columns[1].get_text(strip=True)
            risk_factor = columns[2].get_text(strip=True)
            cvss_score = columns[3].get_text(strip=True)

            # CSV'ye yaz
            writer.writerow({
                'Bulgu Başlığı': title,
                'IP Adresi:Portu': ip_port,
                'Risk Faktörü': risk_factor,
                'CVSS Skoru': cvss_score
            })
            vulnerabilities_found = True

    if vulnerabilities_found:
        print(f'Rapor başarıyla {output_csv_file} dosyasına yazıldı.')
    else:
        print('Hiç zafiyet bulunamadı.')
