from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os, time
from datetime import datetime
from time import sleep
from .models import Zone, Infected, Metric, Deceased, Source, Update
from django.conf import settings
from .table import updateDOCX



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
    
    # click the 'Deaths" option
    try:
      option = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Deaths')]")))
    except:
      option = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'react-select-6-option-1')))
    option.click()
    
    # Fetch the newly displayed value
    new_deceased_el = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.sc-fzoJMP.fQymcb')))
    new_deceased = int(new_deceased_el.text.replace(',', ''))
    print(f"\nGloabl ∆Todesfälle: {new_deceased}")
    print("\n")

    # Update database
    infected = Infected.objects.get(zone=Zone.objects.get(name="Global"))
    infected.new = total_infected - infected.total
    infected.total = total_infected
    infected.save()
    deceased = Deceased.objects.get(zone=Zone.objects.get(name="Global"))
    deceased.new = total_deceased - deceased.total
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
  
  driver.get("https://raw.githubusercontent.com/openZH/covid_19/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_ZH_total.csv")

  try:
    content = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "pre")))
    
    yesterday_substring = [i for i in content.text.split('\n') if i][-2]
    yesterday_array = yesterday_substring.split(",")
    yesterday_infected = number(yesterday_array[4])
    yesterday_deceased = number(yesterday_array[10])
    print("Zürich yesterday infected: " + str(yesterday_infected))
    print("Zürich yesterday deceased: " + str(yesterday_deceased))
    
    today_substring = [i for i in content.text.split('\n') if i][-1]
    today_array = today_substring.split(",")
    today_infected = number(today_array[4])
    today_deceased = number(today_array[10])
    print("Zürich today infected: " + str(today_infected))
    print("Zürich totday deceased: " + str(today_deceased))
    
    equivalence1 = (infected.new == today_infected - yesterday_infected)
    equivalence2 = (infected.total == today_infected)
    equivalence3 = (deceased.new == today_deceased - yesterday_deceased)
    equivalence4 = (deceased.total == today_deceased)
    
    if equivalence1 and equivalence2 and equivalence3 and equivalence4:
      print("Zurich data didn't change")
      
    else:
      print('new Zurich data')
      infected = Infected.objects.get(zone=Zone.objects.get(name="Zürich"))
      infected.new = today_infected - yesterday_infected
      infected.total = today_infected
      infected.save()
      
      deceased = Deceased.objects.get(zone=Zone.objects.get(name="Zürich"))
      deceased.new = today_deceased - yesterday_deceased
      deceased.total = today_deceased
      deceased.save()
    
  finally:
    pass
  
  return "Zh scrape is done"


def scrape():

  print(f"Execution start: {datetime.now()}")

  # # Dev mode config
  # PATH="/Users/gautier/Documents/Z/Chromedriver/chromedriver"
  # driver = webdriver.Chrome(PATH)

  # VM config
  user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
  options = webdriver.ChromeOptions()
  options.headless = True
  options.add_argument(f'user-agent={user_agent}')
  options.add_argument("--window-size=1920,1080")
  options.add_argument('--ignore-certificate-errors')
  options.add_argument('--allow-running-insecure-content')
  options.add_argument("--disable-extensions")
  options.add_argument("--proxy-server='direct://'")
  options.add_argument("--proxy-bypass-list=*")
  options.add_argument("--start-maximized")
  options.add_argument('--disable-gpu')
  options.add_argument('--disable-dev-shm-usage')
  options.add_argument('--no-sandbox')
  PATH=f"{settings.BASE_DIR}/staticfiles/chromedriver"
  driver = webdriver.Chrome(PATH, options=options)
    

  WHO_scrape(driver)
  ncov_scrape(driver)
  zh_scrape(driver)

  driver.quit()

  updateDOCX()

  Update.objects.create(time=f"{str(datetime.today().day).zfill(2)}.{str(datetime.today().month).zfill(2)}.{datetime.today().year} um {str(datetime.today().hour).zfill(2)}:{str(datetime.today().minute).zfill(2)}")

  print(f"Execution end: {datetime.now()}")
