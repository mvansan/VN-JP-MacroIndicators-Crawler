from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import datetime
import os
import sys
import subprocess

def get_last_available_date():
    try:
        df = pd.read_csv("data/raw/vn_interbank_interest.csv")
        df['date'] = pd.to_datetime(df['Ngày áp dụng'], format='%d/%m/%Y')
        return df['date'].max().date()
    except:
        return datetime.date(2020, 1, 1)  # Default start date if no data exists

def run_cleaner():
    subprocess.run([sys.executable, "cleaner/vn_interbank_cleaner.py"])

def run_visualizer():
    subprocess.run([sys.executable, "visualize/vn_interbank_interest_visualizer.py"])

def crawl_interbank_interest():
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')  # Sử dụng headless mode mới
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')  # Set window size
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
        
        driver.get("https://sbv.gov.vn/webcenter/portal/vi/menu/rm/ls/lsttlnh")
        wait = WebDriverWait(driver, 30)

        # Đợi trang load hoàn toàn
        time.sleep(10)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

        # Ensure data/raw directory exists
        os.makedirs("data/raw", exist_ok=True)
        csv_file = "data/raw/vn_interbank_interest.csv"
        header_written = os.path.exists(csv_file) and os.path.getsize(csv_file) > 0

        start_date = get_last_available_date() + datetime.timedelta(days=1)
        end_date = datetime.date.today()
        current_date = start_date

        if current_date > end_date:
            print("No new data to crawl")
            return

        print(f"Starting crawl from {start_date} to {end_date}")

        while current_date <= end_date:
            date_str = current_date.strftime("%d/%m/%Y")
            print(f"Current date: {date_str}")
            try:
                # Đợi và tìm input fields
                input_from = wait.until(EC.presence_of_element_located((By.ID, "T:oc_5531706273region:id1::content")))
                input_to = wait.until(EC.presence_of_element_located((By.ID, "T:oc_5531706273region:id4::content")))
                
                # Clear và nhập ngày
                driver.execute_script("arguments[0].value = '';", input_from)
                driver.execute_script("arguments[0].value = '';", input_to)
                input_from.send_keys(date_str)
                input_to.send_keys(date_str)
                time.sleep(2)
                
                # Click nút tìm kiếm
                search_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="T:oc_5531706273region:cb1"]')))
                driver.execute_script("arguments[0].click();", search_btn)
                time.sleep(15)  # Tăng thời gian chờ
                
                # Kiểm tra kết quả
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.x1g.x1h, table[id*='region:t1'] tbody tr")))
                
                # Kiểm tra có dữ liệu không
                no_data_divs = driver.find_elements(By.CSS_SELECTOR, "div.x1g.x1h")
                if no_data_divs and any("Không có dữ liệu" in div.text for div in no_data_divs):
                    print(f"No data for {date_str}")
                    current_date += datetime.timedelta(days=1)
                    continue

                # Tìm và xử lý dữ liệu
                all_xem_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(text(), 'Xem')]")))
                if not all_xem_buttons:
                    print(f"No 'Xem' buttons found for {date_str}")
                    current_date += datetime.timedelta(days=1)
                    continue

                for xem_button in all_xem_buttons:
                    try:
                        # Click nút Xem
                        driver.execute_script("arguments[0].click();", xem_button)
                        time.sleep(15)  # Tăng thời gian chờ
                        
                        # Lấy dữ liệu
                        ngay_ap_dung = wait.until(EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="T:oc_5531706273region:j_id__ctru7pc9"]/table/tbody/tr/td[2]/table/tbody/tr[2]/td/span[2]')
                        )).text.strip()
                        
                        lai_suat = wait.until(EC.presence_of_element_located(
                            (By.XPATH, '//*[@id="T:oc_5531706273region:j_id__ctru7pc9"]/table/tbody/tr/td[2]/table/tbody/tr[4]/td[2]/span[1]')
                        )).text.strip()
                        
                        print(f"Ngày: {ngay_ap_dung}, Lãi suất: {lai_suat}")
                        
                        # Lưu dữ liệu
                        df = pd.DataFrame([{ "Ngày áp dụng": ngay_ap_dung, "Lãi suất qua đêm": lai_suat }])
                        if not header_written:
                            df.to_csv(csv_file, mode='w', index=False, encoding="utf-8-sig")
                            header_written = True
                        else:
                            df.to_csv(csv_file, mode='a', index=False, header=False, encoding="utf-8-sig")
                        
                        # Quay lại trang kết quả
                        back_button = wait.until(EC.element_to_be_clickable(
                            (By.XPATH, '//*[@id="T:oc_5531706273region:j_id__ctru11pc9"]')
                        ))
                        driver.execute_script("arguments[0].click();", back_button)
                        time.sleep(5)
                        
                    except Exception as e:
                        print(f"Error processing data for {date_str}: {str(e)}")
                        continue
                
                current_date += datetime.timedelta(days=1)
                
            except Exception as e:
                print(f"Error for date {date_str}: {str(e)}")
                current_date += datetime.timedelta(days=1)
                continue

    finally:
        driver.quit()

if __name__ == "__main__":
    crawl_interbank_interest()
    run_cleaner()
    run_visualizer()
