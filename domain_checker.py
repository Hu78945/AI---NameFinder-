# -*- coding: utf-8 -*-
"""Untitled5.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZIO6Y9lVNKzSRgS-_CIZ8H9ophYl-W1k
"""

import requests
import openpyxl
import os


# Replace with your GoDaddy API Key and Secret
API_KEY = '3mM44UdBzbqpSr_N6PdH8XcwBeqd2e4gWnjn8'
API_SECRET = '8n2xgP5i6vrchWAxj5iYt5'

# Function to check domain availability and pricing
def check_domain_availability_and_pricing(domain):
    url = f'https://api.ote-godaddy.com/v1/domains/available?domain={domain}.com'

    headers = {
        'Authorization': f'sso-key {API_KEY}:{API_SECRET}',
        "accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    print(response.content)

    if response.status_code == 200:
        data = response.json()
        available = data.get('available', False)
        pricing = data.get('price', 'N/A')  # Adjust if the pricing information is in a different field
        return available, pricing
    else:
        print(f"Error checking domain {domain}: {response.text}")
        return None, None

# Function to save results to an Excel file
def save_to_excel(data, filename='domain_availability.xlsx'):
    # Check if the file exists
    if os.path.exists(filename):
        # Load existing workbook and worksheet
        wb = openpyxl.load_workbook(filename)
        ws = wb.active
    else:
        # Create new workbook and worksheet
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Domains"
        # Create header
        ws.append(["Domain", "Available", "Price"])

    # Add data
    for entry in data:
        ws.append([entry['domain'], "Yes" if entry['available'] else "No", entry['price']])

    # Save the workbook
    wb.save(filename)
    print(f"Results appended to {filename}")
# Main function that accepts domains as parameters
def main(*domains):
    results = []

    for domain in domains:
        available, price = check_domain_availability_and_pricing(domain)
        results.append({'domain': domain, 'available': available, 'price': price})

    save_to_excel(results)

# Example usage
if __name__ == '__main__':
    # Call the main function with domain names as parameters
    main("mango")