# from __future__ import absolute_import, unicode_literals
# from celery import shared_task

from .models import Zone, Infected, Metric, Deceased, Source
import time
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def number(some_string):
  return int(some_string.replace(',', '').replace(' ', ''))


def WHO_scrape():

  PATH = "/Users/gautier/Documents/Z/Chromedriver/chromedriver"
  driver = webdriver.Chrome(PATH)

  driver.get("https://covid19.who.int")

  try:
    total_infected_el = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.XPATH, "(//span[@class='sc-fzoJMP fQymdt'])")))
    total_infected = int(total_infected_el.text.replace(',', ''))
    print(f"\nGlobal Bestätigte Infektionen: {total_infected}")

    new_infected_el = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, '.sc-fzoJMP.fQymcb')))
    new_infected = int(new_infected_el.text.replace(',', ''))
    print(f"\nGloabl ∆Infektionen: {new_infected}")

    total_deceased_el = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.XPATH, "(//span[@class='sc-fzoJMP fQymdt'])[2]")))
    total_deceased = int(total_deceased_el.text.replace(',', ''))
    print(f"\nGlobal Bestätigte Infektionen: {total_deceased}")

    # click the dropdown
    dropdown = driver.find_element_by_xpath(
      "(//div[@class='dropdown__control css-yk16xz-control'])")
    dropdown.click()
    # click the 'Deaths" option
    option = driver.find_element_by_id("react-select-6-option-1")
    option.click()
    # Fetch the newly displayed value
    new_deceased_el = driver.find_element_by_css_selector(
      ".sc-fzoJMP.fQymcb")
    new_deceased = int(new_deceased_el.text.replace(',', ''))
    print(f"\nGloabl ∆Todesfälle: {new_deceased}")
    print("\n")

    # Update database

    infected = Infected.objects.get(zone=Zone.objects.get(name="Global"))
    infected.total = total_infected
    infected.new = new_infected
    infected.save()
    deceased = Deceased.objects.get(zone=Zone.objects.get(name="Global"))
    deceased.total = total_deceased
    deceased.new = new_deceased
    deceased.save()

  finally:
    driver.quit()
  driver.quit()
  return "WHO_scrape is done"


def ncov_scrape():

  PATH = "/Users/gautier/Documents/Z/Chromedriver/chromedriver"
  driver = webdriver.Chrome(PATH)

  driver.get("https://ncov2019.live/data")

  # returns a cell value from a given row and the class name of the targetted column
  def cell_val(row, column_class):
    col = row.find_element_by_css_selector(column_class)
    cell = col.find_element_by_tag_name("span")
    return cell.text

  # prints infected and deceased values for a given location in a specific table
  def location_data(location, table_title):

    # different process for Europe
    if table_title == "Europe":
      table_title = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, f"//*[contains(text(), '{table_title} COVID-19 Stats')]")))
      table_grandparent = table_title.find_element_by_xpath("../..")
      table = table_grandparent.find_element_by_xpath("../..")

      table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "sortable_table_europe")))
      tbody = table.find_element_by_tag_name("tbody")
      row = tbody.find_element_by_tag_name("tr")

    else:
      # get table
      table_title = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, f"//*[contains(text(), '{table_title} COVID-19 Stats')]")))
      table_grandparent = table_title.find_element_by_xpath("../..")
      table = table_grandparent.find_element_by_xpath("../..")

      # get row
      cell_title = table.find_element_by_xpath(
        f"//span[contains(text(), '{location}')]")
      cell_parent = cell_title.find_element_by_xpath("./..")
      row = cell_parent.find_element_by_xpath("../..")

    # update DBvalues for infected
    total_infected = number(cell_val(row, ".text--green.text--green.sorting_1"))
    print(location + " total infected : " + str(total_infected))
    infected = Infected.objects.get(zone=Zone.objects.get(name="United States"))
    infected.new = total_infected - infected.total
    infected.total = total_infected
    infected.save()

    # update DB values for deceased
    total_deceased = number(cell_val(row, ".text--red.text--red"))
    print(location + " total deaths : " + str(total_deceased))
    deceased = Deceased.objects.get(zone=Zone.objects.get(name="United States"))
    deceased.new = total_deceased - deceased.total
    deceased.total = total_deceased
    deceased.save()

  try:
    location_data('United States', "World")
    location_data("Europe", "Europe")
    location_data("Italy", "World")
    location_data("France", "World")
    location_data("Germany", "World")
    location_data("Austria", "World")
    location_data("Switzerland", "World")
  finally:
    driver.quit()
  driver.quit()
  return "ncov_scrape is done"


def scrape(duration=2):

  while True:
    WHO_scrape()
    ncov_scrape()
    sleep(duration)

  return "DONE"
