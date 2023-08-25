import streamlit as st
import asyncio
from pyppeteer import launch
import json
import pandas as pd
import nest_asyncio

# Create a context manager to run an event loop
@contextmanager
def setup_event_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        yield loop
    finally:
        loop.close()
        asyncio.set_event_loop(None)

# Use the context manager to create an event loop
with setup_event_loop() as loop:

# Apply nest_asyncio to allow nested use of asyncio.run and loop.run_until_complete
nest_asyncio.apply()

# A global list to store extracted data
extracted_data = []

async def intercept_request(req):
    if "interact?" in req.url:
        post_data = req.postData
        try:
            data = json.loads(post_data)
            custom_dimensions = data.get("events", [{}])[0].get("xdm", {}).get("_experience", {}).get("analytics", {}).get("customDimensions", {})

            # Extract eVars
            evars = custom_dimensions.get("eVars", {})
            for key, value in evars.items():
                extracted_data.append({"tag": key, "value": str(value)})

            # Extract props
            props = custom_dimensions.get("props", {})
            for key, value in props.items():
                extracted_data.append({"tag": key, "value": str(value)})

        except json.JSONDecodeError:
            pass

    await req.continue_()

async def scrape_website(url):
    browser = await launch(headless=True, handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False, timeout=30000)  # Increased timeout and added headless mode
    page = await browser.newPage()

    # Setting up request interception
    await page.setRequestInterception(True)
    page.on('request', lambda req: asyncio.ensure_future(intercept_request(req)))

    await page.goto(url)
    await asyncio.sleep(10)  # wait for 10 seconds to ensure all requests are captured

    await browser.close()

    # Convert the extracted data to a pandas DataFrame
    df = pd.DataFrame(extracted_data)

    return df

# Streamlit UI
    st.title("Web Scraper")

    url = st.text_input("Enter the website URL:", "https://www.lenovo.com/us/en/accessories-and-software/")

    if st.button("Scrape"):
        df = loop.run_until_complete(scrape_website(url))
        if df is not None:
            st.write(df)
        else:
            st.write("Error occurred while scraping the website.")









