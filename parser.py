import re
import pandas as pd
from bs4 import BeautifulSoup
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description="Parse vulnerability data from an HTML report and export to Excel and CSV.")
parser.add_argument('input_html', type=str, help="Path to the input HTML file")
parser.add_argument('output_file', type=str, help="Output file name (without extension)")

args = parser.parse_args()

# Load HTML file
with open(args.input_html, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Initialize lists for each column
vulnerabilities = []
ip_ports = []
risk_factors = []
cvss_scores = []

# Find vulnerability sections and corresponding values
for vuln_section in soup.find_all('div', class_='plugin-row'):
    
    # Extract Vulnerability name
    vulnerability = vuln_section.find('td', text=re.compile(r'Vulnerability\s*:'))
    if vulnerability:
        vulnerabilities.append(vulnerability.find_next('td').get_text(strip=True))
    else:
        vulnerabilities.append("N/A")
    
    # Extract IP:Port
    ip_port = vuln_section.find('td', text=re.compile(r'IP Address\s*:'))
    if ip_port:
        ip_ports.append(ip_port.find_next('td').get_text(strip=True))
    else:
        ip_ports.append("N/A")
    
    # Extract Risk Factor
    risk_factor = vuln_section.find('td', text=re.compile(r'Risk Factor\s*:'))
    if risk_factor:
        risk_factors.append(risk_factor.find_next('td').get_text(strip=True))
    else:
        risk_factors.append("N/A")
    
    # Extract CVSS Score
    cvss_score = vuln_section.find('td', text=re.compile(r'CVSS v3\.0 Base Score\s*:'))
    if cvss_score:
        cvss_scores.append(cvss_score.find_next('td').get_text(strip=True))
    else:
        cvss_scores.append("N/A")

# Ensure all lists are of the same length
max_len = max(len(vulnerabilities), len(ip_ports), len(risk_factors), len(cvss_scores))
vulnerabilities.extend(["N/A"] * (max_len - len(vulnerabilities)))
ip_ports.extend(["N/A"] * (max_len - len(ip_ports)))
risk_factors.extend(["N/A"] * (max_len - len(risk_factors)))
cvss_scores.extend(["N/A"] * (max_len - len(cvss_scores)))

# Create a DataFrame and export to Excel and CSV
df = pd.DataFrame({
    'Vulnerability': vulnerabilities,
    'IP:Port': ip_ports,
    'Risk Factor': risk_factors,
    'CVSS v3.0 Base Score': cvss_scores
})

# Output file names
output_excel = f"{args.output_file}.xlsx"
output_csv = f"{args.output_file}.csv"

# Save to Excel and CSV files
df.to_excel(output_excel, index=False)
df.to_csv(output_csv, index=False)

print(f"Files have been generated successfully: {output_excel}, {output_csv}")
