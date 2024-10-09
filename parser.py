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
def get_next_data(row, tag="td"):
    sibling = row.find_next(tag)
    if sibling:
        return sibling.get_text(strip=True)
    return "N/A"

# Find and extract data based on headings
for row in soup.find_all('td', class_='details-header'):
    heading = row.get_text(strip=True)
    
    if "Vulnerability" in heading:
        # Vulnerability data should be right after the heading
        vulnerabilities.append(get_next_data(row, "td"))
    
    elif "Plugin Output" in heading:
        # Assuming IP:Port information is within Plugin Output's tag or below
        port_info = get_next_data(row, "td")
        ip_ports.append(port_info if port_info != "N/A" else "No Port Info")

    elif "Risk Factor" in heading:
        risk_factors.append(get_next_data(row, "td"))

    elif "CVSS v3.0 Base Score" in heading:
        cvss_scores.append(get_next_data(row, "td"))

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
