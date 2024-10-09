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

# Iterate through found headers to get the corresponding data
for header in headers:
    header_text = header.get_text(strip=True)

    # Get the next sibling that contains the relevant data
    data_row = header.find_next_sibling()
    while data_row:
        if 'Vulnerability' in header_text:
            vulnerability = data_row.get_text(strip=True)
            vulnerabilities.append(vulnerability)
            break
        elif 'Plugin Output' in header_text:
            ip_port = data_row.get_text(strip=True)
            ip_ports.append(ip_port)
            break
        elif 'Risk Factor' in header_text:
            risk_factor = data_row.get_text(strip=True)
            risk_factors.append(risk_factor)
            break
        elif 'CVSS v3.0 Base Score' in header_text:
            cvss_score = data_row.get_text(strip=True)
            cvss_scores.append(cvss_score)
            break
        data_row = data_row.find_next_sibling()  # Move to the next sibling if not found

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
