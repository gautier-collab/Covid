from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os, time, datetime
from time import sleep
from .models import Zone, Infected, Metric, Deceased, Source, Update

# from .table import updateDOCX

def number(some_string):
  return int(some_string.replace(',', '').replace(' ', ''))


def WHO_scrape(driver):

  driver.get("https://covid19.who.int")

  try:
    total_infected_el = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "(//span[@class='sc-fzoJMP fQymdt'])")))
    total_infected = int(total_infected_el.text.replace(',', ''))
    print(f"\nGlobal Bestätigte Infektionen: {total_infected}")

    new_infected_el = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.sc-fzoJMP.fQymcb')))
    new_infected = int(new_infected_el.text.replace(',', ''))
    print(f"\nGloabl ∆Infektionen: {new_infected}")

    total_deceased_el = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "(//span[@class='sc-fzoJMP fQymdt'])[2]")))
    total_deceased = int(total_deceased_el.text.replace(',', ''))
    print(f"\nGlobal Bestätigte Infektionen: {total_deceased}")

    # click the dropdown
    dropdown = driver.find_element_by_xpath("(//div[@class='dropdown__control css-yk16xz-control'])")
    dropdown.click()
    
    print("flag 1")
    
    # click the 'Deaths" option
    option = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'react-select-6-option-1')))
    option.click()
    
    print("flag 2")
    
    # Fetch the newly displayed value
    new_deceased_el = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.sc-fzoJMP.fQymcb')))
    new_deceased = int(new_deceased_el.text.replace(',', ''))
    print(f"\nGloabl ∆Todesfälle: {new_deceased}")
    print("\n")

    # Update database
    infected = Infected.objects.get(zone=Zone.objects.get(name="Global"))
    infected.new = total_infected - infected.total
    # infected.new = new_infected
    infected.total = total_infected
    infected.save()
    deceased = Deceased.objects.get(zone=Zone.objects.get(name="Global"))
    deceased.new = total_deceased - deceased.total
    # deceased.new = new_deceased
    deceased.total = total_deceased
    deceased.save()

  finally:
    pass
  
  return "WHO_scrape is done"


def ncov_scrape(driver):

  driver.get("https://ncov2019.live/data")

  # prints infected and deceased values for a given location in a specific table
  def location_data(location, table_title):

    # different process for Europe
    if table_title == "Europe":
      table_title = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{table_title} COVID-19 Stats')]")))
      table_grandparent = table_title.find_element_by_xpath("../..")
      table = table_grandparent.find_element_by_xpath("../..")

      table = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "sortable_table_europe")))
      tbody = table.find_element_by_tag_name("tbody")
      row = tbody.find_element_by_tag_name("tr")

    else:

      # get table
      table_title = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{table_title} COVID-19 Stats')]")))
      table_grandparent = table_title.find_element_by_xpath("../..")
      table = table_grandparent.find_element_by_xpath("../..")

      # get row
      cell_title = table.find_element_by_xpath(
        f"//span[contains(text(), '{location}')]")
      cell_parent = cell_title.find_element_by_xpath("./..")
      row = cell_parent.find_element_by_xpath("../..")

    # update DBvalues for infected
    import re
    infected_string = re.search('green sorting_1" data-order="(.*)"><div class', row.get_attribute('innerHTML')).group(1)
    total_infected = number(infected_string)
    infected = Infected.objects.get(zone=Zone.objects.get(name=location))
    infected.new = total_infected - infected.total
    infected.total = total_infected
    infected.save()
    print(location + " total infected : " + str(total_infected))

    # update DB values for deceased
    deceased_string = re.search('text--red" data-order="(.*)"><div class', row.get_attribute('innerHTML')).group(1)
    total_deceased = number(deceased_string)
    deceased = Deceased.objects.get(zone=Zone.objects.get(name=location))
    deceased.new = total_deceased - deceased.total
    deceased.total = total_deceased
    deceased.save()
    print(location + " total deceased : " + str(total_deceased))

  try:
    location_data('United States', "World")
    location_data("Europe", "Europe")
    location_data("Italy", "World")
    location_data("France", "World")
    location_data("Germany", "World")
    location_data("Austria", "World")
    location_data("Switzerland", "World")
    
  finally:
    pass
  
  return "ncov_scrape is done"

def zh_scrape(driver):
  
  driver.get("https://www.zh.ch/de/gesundheit/coronavirus.html")

  try:
    header_1 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), 'Neue positive Zustände in den letzten 24 Stunden')]")))
    row_1 = header_1.find_element_by_xpath("./..")
    data_1 = row_1.find_elements_by_tag_name("strong")
    new_infected = number(data_1[0].text)
    print("Zürich new infected: " + str(new_infected))
    
    infected = Infected.objects.get(zone=Zone.objects.get(name="Zürich"))
    infected.new = new_infected
    infected.total = infected.total + new_infected
    infected.save()
    
    header_2 = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), 'Verstorbene seit Pandemiebeginn')]")))
    row_2 = header_2.find_element_by_xpath("./..")
    data_2 = row_2.find_elements_by_tag_name("strong")
    total_deceased = number(data_2[0].text)
    print("Zürich total deceased: " + str(total_deceased))
    
    deceased = Deceased.objects.get(zone=Zone.objects.get(name="Zürich"))
    deceased.new = total_deceased - deceased.total
    deceased.total = total_deceased
    deceased.save()
    
  finally:
    pass
  
  return "Zh scrape is done"


def scrape():

  print(f"Execution start: {datetime.datetime.now()}")

  # # Dev mode config
  # PATH="/Users/gautier/Documents/Z/Chromedriver/chromedriver"
  # driver = webdriver.Chrome(PATH)

  # Prod mode config
  chrome_options = webdriver.ChromeOptions()
  chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--disable-dev-shm-usage")
  chrome_options.add_argument("--no-sandbox")
  driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

  WHO_scrape(driver)
  ncov_scrape(driver)
  zh_scrape(driver)

  driver.quit()

  # updateDOCX()

  Update.objects.create(time=datetime.datetime.now())

  print(f"Execution end: {datetime.datetime.now()}")
