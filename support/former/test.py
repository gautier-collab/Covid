from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH="/Users/gautier/Documents/Z/Chromedriver/chromedriver" # might have to add .exe extension
driver = webdriver.Chrome(PATH)

driver.get("https://covid19.who.int")

time.sleep(5)

# link = driver.find_element_by_class_name("dropdown__control dropdown__control--is-focused dropdown__control--menu-is-open css-1pahdxg-control")
link = driver.find_element_by_xpath("(//div[@class='dropdown__control css-yk16xz-control'])")
link.click()
option = driver.find_element_by_id("react-select-6-option-1")
option.click()
new_deaths = driver.find_element_by_css_selector(".sc-fzoJMP.fQymcb")
print(new_deaths.text)
    
# infected = driver.find_element_by_css_selector('.sc-fzoJMP.fQymcb')
# infected = driver.find_element_by_xpath("(//span[@class='sc-fzoJMP fQymdt'])[2]")
# print(infected.text)

# try:
#     infected = driver.find_element_by_xpath("(//div[@class='sc-AxjAm'])[1]")
#     print(infected.text)

#     # infected = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS("(//input[@class='sc-fzoJMP'])[1]"))))
#     # print(infected.text)

#     # results = center_col.find_elements_by_tag_name("h3")
#     # for result in results:
#     # print(result.text)

# finally:
#     driver.quit()

# driver.quit()
