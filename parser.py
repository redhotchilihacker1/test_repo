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

# Helper function to get the next sibling text
def get_next_data(row, pattern=None):
    sibling = row.find_next_sibling('div')
    if sibling:
        return sibling.get_text(strip=True)
    return "N/A"

# Extract data from 'Vulnerability' section
for vulnerability_section in soup.find_all('div', class_='details-header'):
    if 'Vulnerability' in vulnerability_section.get_text(strip=True):
        vulnerability_data = vulnerability_section.find_next('div', class_='plugin-row-header')
        if vulnerability_data:
            vulnerabilities.append(vulnerability_data.get_text(strip=True))
        else:
            vulnerabilities.append("N/A")
    # Extract IP:Port information
    elif "Plugin Output" in vulnerability_section.get_text(strip=True):
        port_info = vulnerability_section.find_next('h2')
        if port_info:
            ip_ports.append(port_info.get_text(strip=True))
        else:
            ip_ports.append("N/A")
    # Extract Risk Factor
    elif "Risk Factor" in vulnerability_section.get_text(strip=True):
        risk_factor_data = vulnerability_section.find_next('div', class_='plugin-row')
        if risk_factor_data:
            risk_factors.append(risk_factor_data.get_text(strip=True))
        else:
            risk_factors.append("N/A")
    # Extract CVSS Base Score
    elif "CVSS v3.0 Base Score" in vulnerability_section.get_text(strip=True):
        cvss_data = vulnerability_section.find_next('div', class_='plugin-row')
        if cvss_data:
            cvss_scores.append(cvss_data.get_text(strip=True))
        else:
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
