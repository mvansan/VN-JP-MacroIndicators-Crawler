from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import re
import os
import sys
import pandas as pd
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_last_available_date():
    try:
        df = pd.read_csv("data/raw/jp_cpi.csv")
        df['date'] = pd.to_datetime(df['Month/Year'], format='%m/%Y')
        last_date = df['date'].max()
        return last_date.year, last_date.month
    except Exception as e:
        print(f"Error reading last available date: {str(e)}")
        return 2020, 1

def crawl_jp_cpi():
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
    browser = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Set user agent
        browser.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

        url = 'https://www.e-stat.go.jp/en/dbview?sid=0003427113'
        browser.get(url)
        wait = WebDriverWait(browser, 20)

        time.sleep(3)

        try:
            area_select = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'select.js-top_area-matter_items_select')))[0]
            browser.execute_script("arguments[0].value = '00000'; arguments[0].dispatchEvent(new Event('change'));", area_select)
            time.sleep(3)

            selects = browser.find_elements(By.CSS_SELECTOR, 'select.js-top_area-matter_items_select')
            if len(selects) < 2:
                print("Error: Could not find month selector")
                return False
            month_select = selects[1]

            options = month_select.find_elements(By.TAG_NAME, 'option')
            month_list = []
            for opt in options:
                value = opt.get_attribute('value')
                title = opt.get_attribute('data-title')
                if value and title:
                    month_list.append((value, title))

            month_pattern = re.compile(r'^(Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\. (\d{4})$|^(May) (\d{4})$')
            filtered_month_list = []
            for v, t in month_list:
                m = month_pattern.match(t)
                if m:
                    filtered_month_list.append((v, t))
            month_list = filtered_month_list

            if not month_list:
                print("Error: No valid month options found")
                return False

            start_year, start_month = get_last_available_date()
            current_date = datetime.now()
            end_year = current_date.year
            end_month = current_date.month

            print(f"Last available data: {start_month}/{start_year}")
            print(f"Current date: {end_month}/{end_year}")

            try:
                next_month = start_month + 1
                next_year = start_year
                if next_month > 12:
                    next_month = 1
                    next_year += 1
                
                month_map = {'01':'Jan.','02':'Feb.','03':'Mar.','04':'Apr.','05':'May','06':'Jun.',
                            '07':'Jul.','08':'Aug.','09':'Sep.','10':'Oct.','11':'Nov.','12':'Dec.'}
                next_month_name = month_map[f"{next_month:02d}"]
                
                start_idx = next(i for i, (v, t) in enumerate(month_list) if f"{next_month_name} {next_year}" in t)
                month_list = month_list[:start_idx+1]
                
                if not month_list:
                    print("No new data to crawl")
                    return False
                    
            except StopIteration as e:
                print(f"Error finding date range: {e}")
                return False

            try:
                existing_df = pd.read_csv("data/raw/jp_cpi.csv")
                existing_data = existing_df.values.tolist()
            except Exception as e:
                print(f"Error reading existing data: {str(e)}")
                existing_data = []

            new_data_found = False
            results = []
            
            os.makedirs("data/raw", exist_ok=True)
            
            for value, title in month_list:
                try:
                    Select(month_select).select_by_value(value)
                    time.sleep(3)
                    apply_btn = browser.find_element(By.CSS_SELECTOR, 'button.js-top_area-done')
                    apply_btn.click()
                    time.sleep(3)
                    
                    error_msg = browser.find_elements(By.CSS_SELECTOR, '.error_message')
                    if error_msg and "No data" in error_msg[0].text:
                        continue
                        
                    cell = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/section/div[3]/div/div/div[2]/div[2]/div[1]/div[1]/div/table/tbody/tr[1]/td[2]')))
                    cpi_value = cell.text.strip()
                    
                    if not cpi_value:
                        continue
                        
                except Exception as e:
                    print(f'Error when fetching data {title}: {e}')
                    continue

                try:
                    m = month_pattern.match(title)
                    if m:
                        if m.group(1):
                            month = m.group(1)
                            year = m.group(2)
                        else:
                            month = m.group(3)
                            year = m.group(4)
                        
                        month_map = {
                            'Jan.': '01', 'Feb.': '02', 'Mar.': '03', 'Apr.': '04',
                            'May': '05', 'Jun.': '06', 'Jul.': '07', 'Aug.': '08',
                            'Sep.': '09', 'Oct.': '10', 'Nov.': '11', 'Dec.': '12'
                        }
                        
                        if month != 'May':
                            month = f"{month}."
                        
                        month_num = month_map[month]
                        formatted = f'{month_num}/{year}'
                    else:
                        continue
                        
                except Exception as e:
                    print(f"Error formatting date for {title}: {e}")
                    continue

                if not any(entry[0] == formatted for entry in existing_data):
                    new_data_found = True
                    print(f"Found new data for {formatted}: {cpi_value}")
                    results.append([formatted, cpi_value])
                    
                    all_data = existing_data + results
                    all_data.sort(key=lambda x: datetime.strptime(x[0], "%m/%Y"))
                    with open("data/raw/jp_cpi.csv", "w", newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow(['Month/Year', 'CPI'])
                        writer.writerows(all_data)
                    
                time.sleep(1.5)

            if not new_data_found:
                print("\nNo new data found. Stopping process.")
                return False

            print("Data saved successfully!")
            return True

        except Exception as e:
            print(f"Error during crawling: {str(e)}")
            return False

    finally:
        browser.quit()

if __name__ == "__main__":
    success = crawl_jp_cpi()
    sys.exit(0 if success else 1)
