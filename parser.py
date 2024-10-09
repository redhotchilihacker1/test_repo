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

# Look for the relevant headers and extract data
for header in soup.find_all('div', class_='details-header'):
    header_text = header.get_text(strip=True)

    if "Vulnerability" in header_text:
        # Get the next sibling which should contain the vulnerability name
        vulnerability_row = header.find_next('div')
        if vulnerability_row:
            vulnerabilities.append(vulnerability_row.get_text(strip=True))
        else:
            vulnerabilities.append("N/A")
    
    elif "Plugin Output" in header_text:
        # Get the next sibling that contains the IP:Port info
        plugin_output_row = header.find_next('div')
        if plugin_output_row:
            ip_ports.append(plugin_output_row.get_text(strip=True))
        else:
            ip_ports.append("N/A")
    
    elif "Risk Factor" in header_text:
        # Get the risk factor information
        risk_factor_row = header.find_next('div')
        if risk_factor_row:
            risk_factors.append(risk_factor_row.get_text(strip=True))
        else:
            risk_factors.append("N/A")
    
    elif "CVSS v3.0 Base Score" in header_text:
        # Get the CVSS score
        cvss_row = header.find_next('div')
        if cvss_row:
            cvss_scores.append(cvss_row.get_text(strip=True))
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
