from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH="/Users/gautier/Documents/Z/Chromedriver/chromedriver"
driver = webdriver.Chrome(PATH)

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
