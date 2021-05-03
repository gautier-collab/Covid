import time, datetime
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Dev mode config
PATH="/Users/gautier/Documents/Z/Chromedriver/chromedriver"
driver = webdriver.Chrome(PATH)

# # Prod mode config
# import os
# chrome_options = webdriver.ChromeOptions()
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--no-sandbox")
# driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)


driver.get("https://www.zh.ch/de/gesundheit/coronavirus.html")

try:
  header_1 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), 'Neue positive Zustände in den letzten 24 Stunden')]")))
  row_1 = header_1.find_element_by_xpath("./..")
  data_1 = row_1.find_elements_by_tag_name("strong")
  new_infected = data_1[0].text
  print("Zürich new infected: " + new_infected)
  
  header_2 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), 'Verstorbene seit Pandemiebeginn')]")))
  row_2 = header_2.find_element_by_xpath("./..")
  data_2 = row_2.find_elements_by_tag_name("strong")
  total_deceased = data_2[0].text
  print("Zürich total deceased: " + total_deceased)
  

  # new_infected = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.sc-fzoJMP.fQymcb')))
  # print(f"\nGloabl ∆Infektionen: {new_infected.text}")

  # total_deaths = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "(//span[@class='sc-fzoJMP fQymdt'])[2]")))
  # print(f"\nGlobal Bestätigte Infektionen: {total_deaths.text}")

  # # click the dropdown
  # dropdown = driver.find_element_by_xpath("(//div[@class='dropdown__control css-yk16xz-control'])")
  # dropdown.click()
  # # click the 'Deaths" option
  # option = driver.find_element_by_id("react-select-6-option-1")
  # option.click()
  # # Fetch the newly displayed value
  # new_deaths = driver.find_element_by_css_selector(".sc-fzoJMP.fQymcb")
  # print(f"\nGloabl ∆Todesfälle: {new_deaths.text}")
  # print("\n")

finally:
  pass

driver.quit()