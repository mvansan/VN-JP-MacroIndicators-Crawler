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

options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://finance.vietstock.vn/du-lieu-vi-mo/52/cpi.htm?languageid=2"
driver.get(url)
time.sleep(5)  

driver.execute_script("window.scrollBy(0, 1000);")  

time.sleep(1)

start_year = 2020
end_year = 2025
end_month_2025 = 4

all_cpi = []

for year in range(start_year, end_year + 1):
    from_month = "1"
    to_month = "12"
    if year == end_year:
        to_month = str(end_month_2025)
    from_year = str(year)
    to_year = str(year)

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

    if year == end_year:
        months = range(1, end_month_2025 + 1)
    else:
        months = range(1, 13)
    for i, value in zip(months, cpi_values):
        month_year = f"{i:02d}/{year}"
        all_cpi.append([month_year, value])

with open("vn_cpi.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Month/Year", "CPI"])
    writer.writerows(all_cpi)

driver.quit()
