import requests
from bs4 import BeautifulSoup
import pandas as pd
import pdfplumber

# Function to scrape HTML data
def scrape_html_data(url, tag, class_name=None):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        if class_name:
            elements = soup.find_all(tag, class_=class_name)
        else:
            elements = soup.find_all(tag)
        return [element.text.strip() for element in elements]
    except Exception as e:
        print(f"Error scraping HTML data from {url}: {e}")
        return []

# Function to scrape PDF data
def scrape_pdf_data(pdf_url):
    try:
        pdf_path = "council_data.pdf"
        response = requests.get(pdf_url)
        with open(pdf_path, 'wb') as file:
            file.write(response.content)
        with pdfplumber.open(pdf_path) as pdf:
            data = [page.extract_text() for page in pdf.pages]
        return data
    except Exception as e:
        print(f"Error scraping PDF data from {pdf_url}: {e}")
        return []

# Function to save data to CSV
def save_to_csv(data, filename):
    try:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving data to {filename}: {e}")

# Example: Scrape Chennai Corporation data
def scrape_chennai_data():
    url = "https://chennaicorporation.gov.in/gcc/council/council-address/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')  # Locate the table
    rows = table.find_all('tr')
    data = [[col.text.strip() for col in row.find_all('td')] for row in rows]
    save_to_csv(data, "chennai_council.csv")

# Example: Scrape Coimbatore Corporation data
def scrape_coimbatore_data():
    pdf_url = "https://www.ccmc.gov.in/img/upload/CCMC-Councilors%20Details%202022.pdf"
    data = scrape_pdf_data(pdf_url)
    for page in data:
        print(page)

# Run scrapers
scrape_chennai_data()
scrape_coimbatore_data()
