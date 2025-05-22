from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# url = "https://vn.investing.com/rates-bonds/vietnam-5-year-bond-yield-historical-data" #use for vietnam
url = "https://www.investing.com/rates-bonds/japan-5-year-bond-yield-historical-data" #use for japan
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

start_date_input.clear()
start_date_input.send_keys('01/02/2020')
time.sleep(2)

# apply_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Áp dụng')]") #use for vietnam
apply_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Apply')]") #use for japan
driver.execute_script("arguments[0].click();", apply_button)
time.sleep(10)

rows = driver.find_elements(By.CSS_SELECTOR, 'table tr')
# with open('data/vn_bond_yield.csv', 'w', newline='', encoding='utf-8') as f: #use for vietnam
with open('data/jp_bond_yield.csv', 'w', newline='', encoding='utf-8') as f: #use for japan
    writer = csv.writer(f)
    writer.writerow(['date', 'yield'])
    last_date = None
    for i in range(1, len(rows)):
        try:
            row = rows[i]
            date_td = row.find_element(By.CSS_SELECTOR, 'td.sticky.left-0 time')
            date_val = date_td.get_attribute('datetime')
            percent_td = row.find_elements(By.CSS_SELECTOR, 'td')[-1]
            percent_val = percent_td.text.strip()
            writer.writerow([date_val, percent_val])
            print(date_val, percent_val)
            last_date = date_val
            driver.execute_script('arguments[0].scrollIntoView({block: "end"});', row)
            time.sleep(0.15)
            if date_val.endswith('01/01/2020'):
                break
        except Exception as e:
            print('Erorr when crawl row:', e)
            continue

driver.quit()