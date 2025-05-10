from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import re

chrome_options = Options()
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

browser = webdriver.Chrome(options=chrome_options)

url = 'https://www.e-stat.go.jp/en/dbview?sid=0003427113'
browser.get(url)
wait = WebDriverWait(browser, 20)

time.sleep(3)

area_select = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'select.js-top_area-matter_items_select')))[0]

browser.execute_script("arguments[0].value = '00000'; arguments[0].dispatchEvent(new Event('change'));", area_select)
time.sleep(3)

selects = browser.find_elements(By.CSS_SELECTOR, 'select.js-top_area-matter_items_select')
if len(selects) < 2:
    browser.quit()
    exit(1)
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
start_idx = next(i for i, (v, t) in enumerate(month_list) if 'Mar. 2025' in t)
end_idx = next(i for i, (v, t) in enumerate(month_list) if 'Jan. 2020' in t)
month_list = month_list[start_idx:end_idx+1]

csv_file = 'data/jp_cpi.csv'
results = []
for value, title in month_list:
    Select(month_select).select_by_value(value)
    time.sleep(0.5)
    apply_btn = browser.find_element(By.CSS_SELECTOR, 'button.js-top_area-done')
    apply_btn.click()
    try:
        cell = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/section/div[3]/div/div/div[2]/div[2]/div[1]/div[1]/div/table/tbody/tr[1]/td[2]')))
        cpi_value = cell.text.strip()
    except Exception as e:
        print(f'Erorr when fetching data {title}: {e}')
        cpi_value = ''
    try:
        m = month_pattern.match(title)
        if m.group(1):
            month, year = m.group(1), m.group(2)
        else:
            month, year = m.group(3), m.group(4)
        month_map = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
        month_num = month_map[month]
        formatted = f'{month_num}/{year}'
    except Exception:
        formatted = title
    print(f'{formatted}: {cpi_value}')
    results.insert(0, [formatted, cpi_value])  
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Month/Year', 'CPI'])
        writer.writerows(results)
    time.sleep(1.5)

browser.quit()
