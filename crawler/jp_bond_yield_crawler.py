from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import os
import sys
import subprocess
import pandas as pd
from datetime import datetime, timedelta

def get_last_available_date():
    try:
        df = pd.read_csv("data/raw/jp_bond_yield.csv")
        df['date'] = pd.to_datetime(df['date'])
        last_date = df['date'].max()
        return last_date + timedelta(days=1)
    except:
        return datetime(2020, 1, 1)

def run_cleaner():
    subprocess.run([sys.executable, "cleaner/jp_bond_yield_cleaner.py"])

def run_visualizer():
    subprocess.run([sys.executable, "visualize/jp_bond_yield_visualizer.py"])

def crawl_jp_bond_yield():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = "https://www.investing.com/rates-bonds/japan-5-year-bond-yield-historical-data"
    driver.get(url)
    time.sleep(5)  

    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(5)

    date_pickers = driver.find_elements(By.CSS_SELECTOR, '.shadow-select')
    date_picker = None
    for el in date_pickers:
        try:
            if 'gap-3.5' in el.get_attribute('class') and '-' in el.text:
                date_picker = el
                break
        except Exception:
            continue
    if date_picker is None:
        raise Exception('Not found date picker')
    date_picker.click()

    wait = WebDriverWait(driver, 20)
    start_date_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='date']")))
    print('Date input value:', start_date_input.get_attribute('value'))

    start_date = get_last_available_date()
    current_date = datetime.now()
    
    if start_date > current_date:
        print("No new data to crawl")
        driver.quit()
        return False

    print(f"Starting crawl from {start_date.strftime('%d/%m/%Y')} to {current_date.strftime('%d/%m/%Y')}")

    # Format date for input field (YYYY-MM-DD)
    start_date_input.clear()
    start_date_input.send_keys(start_date.strftime('%Y-%m-%d'))
    time.sleep(2)

    apply_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Apply')]")
    driver.execute_script("arguments[0].click();", apply_button)
    time.sleep(10)

    # Ensure data directory exists
    os.makedirs('data/raw', exist_ok=True)

    try:
        existing_df = pd.read_csv("data/raw/jp_bond_yield.csv")
        existing_data = existing_df.values.tolist()
    except:
        existing_data = []

    rows = driver.find_elements(By.CSS_SELECTOR, 'table tr')
    new_data_found = False
    results = []

    for i in range(1, len(rows)):
        try:
            row = rows[i]
            date_td = row.find_element(By.CSS_SELECTOR, 'td.sticky.left-0 time')
            date_val = date_td.get_attribute('datetime')
            percent_td = row.find_elements(By.CSS_SELECTOR, 'td')[-1]
            percent_val = percent_td.text.strip()
            
            # Convert date_val to datetime for comparison
            date_val_dt = pd.to_datetime(date_val)
            if date_val_dt >= start_date and not any(entry[0] == date_val for entry in existing_data):
                new_data_found = True
                print(f"Found new data for {date_val}: {percent_val}")
                results.append([date_val, percent_val])
            
            driver.execute_script('arguments[0].scrollIntoView({block: "end"});', row)
            time.sleep(0.15)
        except Exception as e:
            print('Error when crawl row:', e)
            continue

    driver.quit()

    if not new_data_found:
        print("\nNo new data found. Stopping process.")
        return False

    print("\nSaving new data...")
    
    all_data = existing_data + results
    all_data.sort(key=lambda x: datetime.strptime(x[0], "%Y-%m-%d"))
    
    with open("data/raw/jp_bond_yield.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(['date', 'yield'])
        writer.writerows(all_data)

    print("Data saved successfully!")
    return True

if __name__ == "__main__":
    success = crawl_jp_bond_yield()
    if success:
        run_cleaner()
        run_visualizer()
    sys.exit(0 if success else 1) 