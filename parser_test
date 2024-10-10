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
dns_names = []
synopsis_list = []
description_list = []
see_also_list = []
solution_list = []

# Function to check if the background is not white (checking both 'background-color' and 'background')
def is_not_white_background(tag):
    style = tag.get('style')
    if style:
        # Check for 'background-color' and 'background'
        background_color_match = re.search(r'background(-color)?:\s*(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|rgb\((\d+),\s*(\d+),\s*(\d+)\))', style)
        if background_color_match:
            color = background_color_match.group(0)
            # Exclude white (#FFFFFF, #FFF, or rgb(255, 255, 255))
            if '255, 255, 255' not in color and '#ffffff' not in color.lower() and '#fff' not in color.lower():
                return True
    return False

# Find the divs with non-white background and extract the cleartext starting with a 5-digit number
for div in soup.find_all('div'):
    if is_not_white_background(div):
        # Check the text inside the current div for a 5-digit number at the start
        text = div.get_text(strip=True)
        if re.match(r'^\d{5}', text):
            vulnerabilities.append(text)

# New fields for DNS Name, Synopsis, Description, See Also, Solution
def extract_text_after_header(header):
    header_tag = soup.find(text=re.compile(header))
    if header_tag:
        next_sibling = header_tag.find_next('div')
        if next_sibling:
            return next_sibling.get_text(strip=True)
    return "N/A"

dns_names.append(extract_text_after_header("DNS Name"))
synopsis_list.append(extract_text_after_header("Synopsis"))
description_list.append(extract_text_after_header("Description"))
see_also_list.append(extract_text_after_header("See Also"))
solution_list.append(extract_text_after_header("Solution"))

# For IP:Port, Risk Factor, CVSS, same logic as before
for header in soup.find_all(['h2', 'h3', 'div'], class_=lambda x: x and 'details-header' in x):
    header_text = header.get_text(strip=True)
    data_row = header.find_next_sibling()
    
    while data_row:
        if 'Plugin Output' in header_text:
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
        data_row = data_row.find_next_sibling()

# Ensure all lists are of the same length
max_len = max(len(vulnerabilities), len(ip_ports), len(risk_factors), len(cvss_scores), len(dns_names))
vulnerabilities.extend(["N/A"] * (max_len - len(vulnerabilities)))
ip_ports.extend(["N/A"] * (max_len - len(ip_ports)))
risk_factors.extend(["N/A"] * (max_len - len(risk_factors)))
cvss_scores.extend(["N/A"] * (max_len - len(cvss_scores)))
dns_names.extend(["N/A"] * (max_len - len(dns_names)))
synopsis_list.extend(["N/A"] * (max_len - len(synopsis_list)))
description_list.extend(["N/A"] * (max_len - len(description_list)))
see_also_list.extend(["N/A"] * (max_len - len(see_also_list)))
solution_list.extend(["N/A"] * (max_len - len(solution_list)))

# Create a DataFrame
df = pd.DataFrame({
    'Vulnerability': vulnerabilities,
    'IP:Port': ip_ports,
    'Risk Factor': risk_factors,
    'CVSS v3.0 Base Score': cvss_scores,
    'DNS Name': dns_names,
    'Synopsis': synopsis_list,
    'Description': description_list,
    'See Also': see_also_list,
    'Solution': solution_list
})

# Output file names
output_excel = f"{args.output_file}.xlsx"
output_csv = f"{args.output_file}.csv"

# Save to Excel and CSV files
df.to_excel(output_excel, index=False)
df.to_csv(output_csv, index=False)

print(f"Files have been generated successfully: {output_excel}, {output_csv}")
