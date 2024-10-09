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

# Helper function to get the RGB value of an element
def get_rgb_color(element):
    style = element.get('style')
    if style:
        match = re.search(r'background-color:\s*rgb\((\d+),\s*(\d+),\s*(\d+)\)', style)
        if match:
            return tuple(map(int, match.groups()))
    return (255, 255, 255)  # Default to white if no color is found

# Iterate through relevant sections to find vulnerability data
for header in soup.find_all(['h2', 'h3', 'div']):
    rgb_color = get_rgb_color(header)

    # Check if the background color is not white
    if rgb_color != (255, 255, 255):
        next_div = header.find_next_sibling('div')
        if next_div:
            if 'Vulnerability' in header.get_text(strip=True):
                vulnerabilities.append(next_div.get_text(strip=True))
            elif 'Plugin Output' in header.get_text(strip=True):
                ip_ports.append(next_div.get_text(strip=True))
            elif 'Risk Factor' in header.get_text(strip=True):
                risk_factors.append(next_div.get_text(strip=True))
            elif 'CVSS v3.0 Base Score' in header.get_text(strip=True):
                cvss_scores.append(next_div.get_text(strip=True))

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
