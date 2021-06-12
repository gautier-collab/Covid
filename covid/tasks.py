import os, time, re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from time import sleep
from django.conf import settings
from .table import updateDOCX
from .models import Zone, Infected, Metric, Deceased, Source, Update, Update_zh


# function executed daily to fetch covid related values from 3 different websites, and register them in the database
def scrape(driver):

  print(f"Execution start: {datetime.now()}")
    
  # execute the web scraping of the 3 websites
  WHO_scrape(driver)
  ncov_scrape(driver)
  zh_scrape(driver)

  # close the browser
  driver.quit()

  # create a new Update instance whose "time" attribute is a string corresponding to the time right now
  Update.objects.create(time = f"{str(datetime.today().day).zfill(2)}.{str(datetime.today().month).zfill(2)}.{datetime.today().year} um {str(datetime.today().hour).zfill(2)}:{str(datetime.today().minute).zfill(2)}")

  # update the Word document downloadable from the UI
  updateDOCX()

  print(f"Execution end: {datetime.now()}")


# returns an integer from a string number containing commas or spaces
def number(some_string):
  return int(some_string.replace(',', '').replace(' ', ''))


# web scraper for the WHO website to register the worldwide values
def WHO_scrape(driver):

  # browser accesses URL of WHO website
  driver.get("https://covid19.who.int")

  try:
    # get total number of infected
    total_infected_el = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "(//span[@class='sc-fzoJMP fQymdt'])")))
    total_infected = int(total_infected_el.text.replace(',', ''))
    print(f"\nGlobal total infected: {total_infected}")

    # get number of new infected
    new_infected_el = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.sc-fzoJMP.fQymcb')))
    new_infected = int(new_infected_el.text.replace(',', ''))
    print(f"Gloabl new infected: {new_infected}")

    # get total number of deceased
    total_deceased_el = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "(//span[@class='sc-fzoJMP fQymdt'])[2]")))
    total_deceased = int(total_deceased_el.text.replace(',', ''))
    print(f"Global total deceased: {total_deceased}")

    # Selenium clicks the dropdown
    dropdown = driver.find_element_by_xpath("(//div[@class='dropdown__control css-yk16xz-control'])")
    dropdown.click()
    
    # Selenium clicks the 'Deaths" option
    try:
      option = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Deaths')]")))
    except:
      option = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'react-select-6-option-1')))
    option.click()
    
    # get number of new deaths
    new_deceased_el = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.sc-fzoJMP.fQymcb')))
    new_deceased = int(new_deceased_el.text.replace(',', ''))
    print(f"Gloabl new deceased: {new_deceased}\n")

    # register fetched values into the database
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
  
  return "End of WHO_scrape execution"


# web scraper for the ncov2019 website to register the national values
def ncov_scrape(driver):

  # function that registers the number infected and deceased for a given country in a specific table (World or Europe) in the database
  def location_data(location, table_title):

    if table_title == "Europe":
      
      # get row of interest
      table = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "sortable_table_europe")))
      tbody = table.find_element_by_tag_name("tbody")
      row = tbody.find_element_by_tag_name("tr")

    else:
      
      # get table of interest
      table_title = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{table_title} COVID-19 Stats')]")))
      table_grandparent = table_title.find_element_by_xpath("../..")
      table = table_grandparent.find_element_by_xpath("../..")

      # get row of interest
      cell_title = table.find_element_by_xpath(f"//span[contains(text(), '{location}')]")
      cell_parent = cell_title.find_element_by_xpath("./..")
      row = cell_parent.find_element_by_xpath("../..")

    # find substring corresponding to number of infected in the row code
    infected_string = re.search('green sorting_1" data-order="(.*)"><div class', row.get_attribute('innerHTML')).group(1)
    total_infected = number(infected_string)
    
    # update infected values of the database
    infected = Infected.objects.get(zone=Zone.objects.get(name=location))
    infected.new = total_infected - infected.total
    infected.total = total_infected
    infected.save()
    print(location + " total infected : " + str(total_infected))

    # find substring corresponding to number of deceased in the row code
    deceased_string = re.search('text--red" data-order="(.*)"><div class', row.get_attribute('innerHTML')).group(1)
    total_deceased = number(deceased_string)
    
    # update deceased values of the database
    deceased = Deceased.objects.get(zone=Zone.objects.get(name=location))
    deceased.new = total_deceased - deceased.total
    deceased.total = total_deceased
    deceased.save()
    print(location + " total deceased : " + str(total_deceased))

  # browser accesses URL of ncov2019
  driver.get("https://ncov2019.live/data")

  # register values of countries of interest
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
  
  return "End of ncov_scrape execution"


# web scraper for the website of Zürich to register cantonal values
def zh_scrape(driver):
  
  # browser accesses URL of Zürich data CSV
  driver.get("https://raw.githubusercontent.com/openZH/covid_19/master/fallzahlen_kanton_total_csv_v2/COVID19_Fallzahlen_Kanton_ZH_total.csv")

  try:
    # get the content of the CSV
    content = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "pre")))
    
    # get the values of today (last row)
    today_substring = [i for i in content.text.split('\n') if i][-1]
    today_array = today_substring.split(",")
    today_infected = number(today_array[4])
    today_deceased = number(today_array[10])
    print("Zürich today infected: " + str(today_infected))
    print("Zürich totday deceased: " + str(today_deceased))
    
    # get the values of yesterday (penultimate row), so we will be able to calculate the 24h evolution
    yesterday_substring = [i for i in content.text.split('\n') if i][-2]
    yesterday_array = yesterday_substring.split(",")
    yesterday_infected = number(yesterday_array[4])
    yesterday_deceased = number(yesterday_array[10])
    print("\nZürich yesterday infected: " + str(yesterday_infected))
    print("Zürich yesterday deceased: " + str(yesterday_deceased))
    
    # get the database objects that should be updated
    infected = Infected.objects.get(zone=Zone.objects.get(name="Zürich"))
    deceased = Deceased.objects.get(zone=Zone.objects.get(name="Zürich"))
    update_zh = Update_zh.objects.all().last()
    
    # detect whether value of yesterday is the same as that of today (if so, assign True)
    equivalence1 = (infected.new == today_infected - yesterday_infected)
    equivalence2 = (infected.total == today_infected)
    equivalence3 = (deceased.new == today_deceased - yesterday_deceased)
    equivalence4 = (deceased.total == today_deceased)
    
    # detect whether the cantonal authorities have updated the values
    if equivalence1 and equivalence2 and equivalence3 and equivalence4:
      print("Zurich data didn't change -> skip update\n")
      
      # no Zürich update so the last update time of Zürich values is now different than that of other locations -> time specific to Zürich update should be displayed
      update_zh.display = True
      update_zh.save()
      
    # cantonal authorities have updated the values so let's fetch them
    else:
      print("New Zurich data -> let's update\n")
      
      # update the number of infected (Zürich)
      infected.new = today_infected - yesterday_infected
      infected.total = today_infected
      infected.save()
      
      # update the number of deceased (Zürich)
      deceased.new = today_deceased - yesterday_deceased
      deceased.total = today_deceased
      deceased.save()
    
      # create a new Update instance (specific to Zürich) whose "time" attribute is a string corresponding to the time right now
      update_zh.time = f"{str(datetime.today().day).zfill(2)}.{str(datetime.today().month).zfill(2)}.{datetime.today().year} um {str(datetime.today().hour).zfill(2)}:{str(datetime.today().minute).zfill(2)}"
      
      # Zürich values are updated (at the same time as those of other locations) so no need to display a time specific to Zürich
      update_zh.display = False
      update_zh.save()
      
  finally:
    pass
  
  return "End of zh_scrape execution"
