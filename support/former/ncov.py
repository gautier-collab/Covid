from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH="/Users/gautier/Documents/Z/Chromedriver/chromedriver"
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
        table_title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{table_title} COVID-19 Stats')]")))
        table_grandparent = table_title.find_element_by_xpath("../..")
        table = table_grandparent.find_element_by_xpath("../..")

        table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "sortable_table_europe")))
        tbody = table.find_element_by_tag_name("tbody")
        row = tbody.find_element_by_tag_name("tr")

    else:
        # get table
        table_title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{table_title} COVID-19 Stats')]")))
        table_grandparent = table_title.find_element_by_xpath("../..")
        table = table_grandparent.find_element_by_xpath("../..")

        # get row
        cell_title = table.find_element_by_xpath(f"//span[contains(text(), '{location}')]")
        cell_parent = cell_title.find_element_by_xpath("./..")
        row = cell_parent.find_element_by_xpath("../..")

    # print total infected
    print(location + " total infected : " + cell_val(row, ".text--green.text--green.sorting_1"))

    # print total deceased
    print(location + " total deaths : " + cell_val(row, ".text--red.text--red"))

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
