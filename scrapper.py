from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define constants
START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"
DRIVER_PATH = "Teacher Activity 6/msedgedriver.exe"

# Set up the webdriver
browser = webdriver.Edge(DRIVER_PATH)
browser.get(START_URL)

# Wait for the page to load
time.sleep(2)

# Define a function to scrape the data
def scrape():
    scraped_data = []
    for i in range(0, 5):  # Looping through a range of 10 pages
        print(f'Scraping page {i+1} ...')
        # Create a BeautifulSoup object
        soup = BeautifulSoup(browser.page_source, "html.parser")
        
        # Find the table with the class "wikitable"
        bright_star_table = soup.find("table", attrs={"class": "wikitable"})

        # Find the table body and rows
        table_body = bright_star_table.find('tbody')
        table_rows = table_body.find_all('tr')

        # Loop through each row and extract the data
        for row in table_rows:
            table_cols = row.find_all('td')
            temp_list = []
            for col_data in table_cols:
                data = col_data.text.strip()
                temp_list.append(data)
            scraped_data.append(temp_list)

    # Extract the required data from the scraped data
    stars_data = []
    for i in range(0, len(scraped_data)):
        Star_names = scraped_data[i][1]
        Distance = scraped_data[i][3]
        Mass = scraped_data[i][5]
        Radius = scraped_data[i][6]
        Lum = scraped_data[i][7]
        required_data = [Star_names, Distance, Mass, Radius, Lum]
        stars_data.append(required_data)

    # Create a Pandas DataFrame and save it to a CSV file
    headers = ['Star_name', 'Distance', 'Mass', 'Radius', 'Luminosity']
    star_df_1 = pd.DataFrame(stars_data, columns=headers)
    star_df_1.to_csv('scraped_data.csv', index=True, index_label="id")

# Call the scrape function
scrape()