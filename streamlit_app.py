import streamlit as st
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller

# A global list to store extracted data
extracted_data = []

def scrape_website(url):
    chromedriver_autoinstaller.install()  # Automatically download and install Chrome Driver
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-accelerated-2d-canvas')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920x1080')

    service = Service(chromedriver_autoinstaller.get_chrome_driver_filename())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)

    # Here, you can use Selenium functions to extract your data.
    # For the sake of example, I'll simulate extracting data from the webpage source.
    # You should replace this with appropriate Selenium code for your needs.
    data = driver.page_source
    extracted_data.append({'data': data[:100]})  # Just taking the first 100 characters for demo purposes

    # Convert the extracted data to a pandas DataFrame
    df = pd.DataFrame(extracted_data)

    driver.quit()

    return df

# Streamlit UI
st.title("Web Scraper using Selenium")

url = st.text_input("Enter the website URL:", "https://www.lenovo.com/us/en/accessories-and-software/")

if st.button("Scrape"):
    df = scrape_website(url)
    st.write(df)








