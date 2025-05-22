from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import pandas as pd
import os
import sys
from datetime import datetime

def get_last_available_date():
    try:
        df = pd.read_csv("data/raw/vn_cpi.csv")
        df['date'] = pd.to_datetime(df['Month/Year'], format='%m/%Y')
        last_date = df['date'].max()
        return last_date.year, last_date.month
    except Exception as e:
        print(f"Error reading last available date: {str(e)}")
        return 2020, 1  

def crawl_vn_cpi():
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Set user agent
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

        url = "https://finance.vietstock.vn/du-lieu-vi-mo/52/cpi.htm?languageid=2"
        driver.get(url)
        time.sleep(5)  

        driver.execute_script("window.scrollBy(0, 1000);")  
        time.sleep(1)

        start_year, start_month = get_last_available_date()
        current_date = datetime.now()
        end_year = current_date.year
        end_month = current_date.month

        if start_year > end_year or (start_year == end_year and start_month >= end_month):
            print("No new data to crawl")
            return False

        print(f"Starting crawl from {start_month}/{start_year} to {end_month}/{end_year}")

        all_cpi = []
        new_data_found = False
        
        try:
            existing_df = pd.read_csv("data/raw/vn_cpi.csv")
            all_cpi = existing_df.values.tolist()
        except Exception as e:
            print(f"Error reading existing data: {str(e)}")
            pass

        for year in range(start_year, end_year + 1):
            from_month = str(start_month) if year == start_year else "1"
            to_month = str(end_month) if year == end_year else "12"
            from_year = str(year)
            to_year = str(year)

            try:
                Select(driver.find_element(By.NAME, "from")).select_by_value(from_month)
                Select(driver.find_element(By.NAME, "fromYear")).select_by_value(from_year)
                Select(driver.find_element(By.NAME, "to")).select_by_value(to_month)
                Select(driver.find_element(By.NAME, "toYear")).select_by_value(to_year)

                view_button = driver.find_element(By.CSS_SELECTOR, "button.btn.bg.m-l")
                view_button.click()
                time.sleep(2)

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//tr[td[text()='Consumer Price Index']]") )
                )

                row = driver.find_element(By.XPATH, "//tr[td[text()='Consumer Price Index']]")
                tds = row.find_elements(By.CSS_SELECTOR, "td.text-right[value]")
                cpi_values = [td.get_attribute("value") for td in tds]

                months = range(int(from_month), int(to_month) + 1)
                for i, value in zip(months, cpi_values):
                    month_year = f"{i:02d}/{year}"
                    if not any(entry[0] == month_year for entry in all_cpi):
                        all_cpi.append([month_year, value])
                        new_data_found = True
                        print(f"Found new data for {month_year}: {value}")

            except Exception as e:
                print(f"Error processing year {year}: {str(e)}")
                continue

        if not new_data_found:
            print("\nNo new data found. Stopping process.")
            return False

        print("\nSaving new data...")
        
        os.makedirs("data/raw", exist_ok=True)
        
        all_cpi.sort(key=lambda x: datetime.strptime(x[0], "%m/%Y"))
        
        with open("data/raw/vn_cpi.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Month/Year", "CPI"])
            writer.writerows(all_cpi)

        print("Data saved successfully!")
        return True

    except Exception as e:
        print(f"Error during crawling: {str(e)}")
        return False

    finally:
        driver.quit()

if __name__ == "__main__":
    success = crawl_vn_cpi()
    sys.exit(0 if success else 1)
