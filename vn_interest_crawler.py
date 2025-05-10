from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import datetime
import os

driver = webdriver.Chrome()
driver.get("https://sbv.gov.vn/webcenter/portal/vi/menu/rm/ls/lsttlnh")

wait = WebDriverWait(driver, 30)

time.sleep(5)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(3)

csv_file = "lai_suat_qua_dem.csv"
header_written = os.path.exists(csv_file) and os.path.getsize(csv_file) > 0

start_date = datetime.date(2023, 1, 1)
end_date = datetime.date(2023, 12, 31)
current_date = start_date

while current_date <= end_date:
    date_str = current_date.strftime("%d/%m/%Y")
    print(f"Current date: {date_str}")
    try:
        input_from = wait.until(EC.presence_of_element_located((By.ID, "T:oc_5531706273region:id1::content")))
        input_to = wait.until(EC.presence_of_element_located((By.ID, "T:oc_5531706273region:id4::content")))
        input_from.clear()
        input_from.send_keys(date_str)
        input_to.clear()
        input_to.send_keys(date_str)
    except Exception as e:
        driver.save_screenshot(f"error_input_date_{date_str}.png")
        current_date += datetime.timedelta(days=1)
        continue

    try:
        search_btn = driver.find_element(By.XPATH, '//*[@id="T:oc_5531706273region:cb1"]')
        search_btn.click()
        time.sleep(12)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.x1g.x1h, table[id*='region:t1'] tbody tr")))
    except Exception as e:
        current_date += datetime.timedelta(days=1)
        continue

    try:
        no_data_divs = driver.find_elements(By.CSS_SELECTOR, "div.x1g.x1h")
        if no_data_divs and any("Không có dữ liệu" in div.text for div in no_data_divs):
            current_date += datetime.timedelta(days=1)
            continue
    except Exception as e:
        current_date += datetime.timedelta(days=1)
        continue

    try:
        crawled = False
        while True:
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table[id*='region:t1'] tbody tr")))
            time.sleep(2)
            all_xem_buttons = driver.find_elements(By.XPATH, "//a[contains(text(), 'Xem')]")
            if not all_xem_buttons:
                break
            try:
                xem_button = all_xem_buttons[0]
                row = xem_button.find_element(By.XPATH, "./ancestor::tr")
                date_element = row.find_element(By.XPATH, ".//td[1]//span[contains(@id, 'content')]")
                date_value = date_element.text.strip()
                if not date_value:
                    continue
                driver.execute_script("arguments[0].click();", xem_button)
                print(f"{date_value}")
                time.sleep(12)
                ngay_ap_dung = wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id=\"T:oc_5531706273region:j_id__ctru7pc9\"]/table/tbody/tr/td[2]/table/tbody/tr[2]/td/span[2]')
                )).text.strip()
                lai_suat = wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id=\"T:oc_5531706273region:j_id__ctru7pc9\"]/table/tbody/tr/td[2]/table/tbody/tr[4]/td[2]/span[1]')
                )).text.strip()
                print(f"Ngày: {ngay_ap_dung}, Lãi suất: {lai_suat}")
                df = pd.DataFrame([{ "Ngày áp dụng": ngay_ap_dung, "Lãi suất qua đêm": lai_suat }])
                if not header_written:
                    df.to_csv(csv_file, mode='w', index=False, encoding="utf-8-sig")
                    header_written = True
                else:
                    df.to_csv(csv_file, mode='a', index=False, header=False, encoding="utf-8-sig")
                back_button = wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id=\"T:oc_5531706273region:j_id__ctru11pc9\"]')
                ))
                driver.execute_script("arguments[0].click();", back_button)
                time.sleep(3)
                crawled = True
                break 
            except Exception as e:
                print(f"{e}")
                break
        if crawled:
            current_date += datetime.timedelta(days=1)
            continue
    except Exception as e:
        print(f"Lỗi khi crawl dữ liệu ngày {date_str}: {e}")
    current_date += datetime.timedelta(days=1)

driver.quit()
