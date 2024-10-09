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

# Find relevant sections based on headers
headers = soup.find_all(['h2', 'h3', 'div'], class_=lambda x: x and 'details-header' in x)

# Extract data for each section
for header in headers:
    header_text = header.get_text(strip=True)

    # Vulnerability: Get the text under the heading
    if 'Vulnerability' in header_text:
        vulnerability_data = header.find_next('div', class_='plugin-row')
        if vulnerability_data:
            vulnerabilities.append(vulnerability_data.get_text(strip=True))
        else:
            print("Warning: Vulnerability data not found after header:", header_text)
            vulnerabilities.append("N/A")

    # IP:Port data
    elif 'Plugin Output' in header_text:
        ip_port_data = header.find_next('h2')
        if ip_port_data:
            ip_ports.append(ip_port_data.get_text(strip=True))
        else:
            print("Warning: IP:Port data not found after header:", header_text)
            ip_ports.append("N/A")

    # Risk Factor
    elif 'Risk Factor' in header_text:
        risk_factor_data = header.find_next('div', class_='plugin-row')
        if risk_factor_data:
            risk_factors.append(risk_factor_data.get_text(strip=True))
        else:
            print("Warning: Risk Factor data not found after header:", header_text)
            risk_factors.append("N/A")

    # CVSS Base Score
    elif 'CVSS v3.0 Base Score' in header_text:
        cvss_data = header.find_next('div', class_='plugin-row')
        if cvss_data:
            cvss_scores.append(cvss_data.get_text(strip=True))
        else:
            print("Warning: CVSS v3.0 Base Score data not found after header:", header_text)
            cvss_scores.append("N/A")

# Ensure all lists are of the same length
max_len = max(len(vulnerabilities), len(ip_ports), len(risk_factors), len(cvss_scores))
vulnerabilities.extend(["N/A"] * (max_len - len(vulnerabilities)))
ip_ports.extend(["N/A"] * (max_len - len(ip_ports)))
risk_factors.extend(["N/A"] * (max_len - len(risk_factors)))
cvss_scores.extend(["N/A"] * (max_len - len(cvss_scores)))

# Create a DataFrame
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
