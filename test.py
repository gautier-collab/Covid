import time, datetime
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# # Dev mode config
# PATH="/Users/gautier/Documents/Z/Chromedriver/chromedriver"
# driver = webdriver.Chrome(PATH)

# Prod mode config
import os
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)


driver.get("https://covid19.who.int")

try:
  total_infected = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "(//span[@class='sc-fzoJMP fQymdt'])")))
  print(f"\nGlobal Bestätigte Infektionen: {total_infected.text}")

  new_infected = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.sc-fzoJMP.fQymcb')))
  print(f"\nGloabl ∆Infektionen: {new_infected.text}")

  total_deaths = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "(//span[@class='sc-fzoJMP fQymdt'])[2]")))
  print(f"\nGlobal Bestätigte Infektionen: {total_deaths.text}")

  # click the dropdown
  dropdown = driver.find_element_by_xpath("(//div[@class='dropdown__control css-yk16xz-control'])")
  dropdown.click()
  # click the 'Deaths" option
  option = driver.find_element_by_id("react-select-6-option-1")
  option.click()
  # Fetch the newly displayed value
  new_deaths = driver.find_element_by_css_selector(".sc-fzoJMP.fQymcb")
  print(f"\nGloabl ∆Todesfälle: {new_deaths.text}")
  print("\n")

finally:
  driver.quit()

driver.quit()

driver.get("https://covid19.who.int")
print("WHO accessed again")

# driver.get("https://ncov2019.live/data")
# print("driver accesses ncov2019")

# driver.get("https://www.worldometers.info/coronavirus/")
# print("driver accesses Worldometer")
driver.quit()