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
            # Zafiyet başlığını bulma
            title_elem = columns[0].find(attrs={'onmouseover': True})
            title = title_elem.get_text(strip=True) if title_elem else None
            
            # IP Adresi:Portu
            ip_port = columns[1].get_text(strip=True)

            # Risk Faktörü
            risk_factor_elem = row.find(string="Risk Factor")
            if risk_factor_elem:
                risk_factor = risk_factor_elem.find_next('td').get_text(strip=True)
            else:
                risk_factor = None
            
            # CVSS Skoru
            cvss_score_elem_v2 = row.find(string="CVSS v2.0 Base Score")
            cvss_score_elem_v3 = row.find(string="CVSS v3.0 Base Score")

            cvss_score = None
            if cvss_score_elem_v2:
                cvss_score = cvss_score_elem_v2.find_next('td').get_text(strip=True)
            elif cvss_score_elem_v3:
                cvss_score = cvss_score_elem_v3.find_next('td').get_text(strip=True)

            # CSV'ye yaz
            if title and ip_port and risk_factor and cvss_score:
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
