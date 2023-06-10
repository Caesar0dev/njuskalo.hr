from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from undetected_chromedriver import Chrome, ChromeOptions
import time
import csv

options = ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument('--headless')
options.add_argument('--disable-gpu')

driver = Chrome(options=options, executable_path=ChromeDriverManager().install())

driver.maximize_window()

component_titles = []
component_links = []
component_types = []
component_ranges = []
component_years = []
component_locations = []
component_posteds = []
component_prices_eur = []
component_prices_kn = []
write_result = []

driver.get("https://www.njuskalo.hr/auti/c-max")

time.sleep(10)

driver.find_element(By.XPATH, '//*[@id="didomi-notice-agree-button"]').click()

totalbox = driver.find_element(By.XPATH, '//*[@id="form_browse_detailed_search"]/div/div[1]/div[7]/div[6]')

subcategories = totalbox.find_elements(By.CLASS_NAME, "entity-body")

for i in range(len(subcategories)):
    title = subcategories[i].find_element(By.TAG_NAME, "h3").text
    # print("Title--> ", title)
    link = subcategories[i].find_element(By.CLASS_NAME, "entity-title").find_element(By.CLASS_NAME, "link").get_attribute("href")
    # print("LInk--> ", link)
    details = subcategories[i].find_element(By.CLASS_NAME, "entity-description-main").text

    ########## split details
    detail_elements = details.split("\n")

    type_range = detail_elements[0].split(",")
    car_type = type_range[0]
    car_range = type_range[1]
    # print("Type-->", car_type)
    # print("Range-->", car_range)

    car_year = detail_elements[1].split(":")[1].replace(".", "")
    # print("Year-->", car_year)

    car_location = detail_elements[2].split(":")[1]
    # print("Location-->", car_location)
    ########### split end

    times = subcategories[i].find_element(By.CLASS_NAME, "date--full").text
    car_posted = times.replace(".", "")
    # print("Posted-->", car_posted)

    price = subcategories[i].find_element(By.CLASS_NAME, "price--hrk").text
    price_eur = price.split("/")[0]
    price_kn = price.split("/")[1]
    # print("Price EUR-->", price_eur)
    # print("Price KN-->", price_kn)
    # print("-------------------------")

    component_titles.append(title)
    component_links.append(link)
    component_types.append(car_type)
    component_ranges.append(car_range)
    component_years.append(car_year)
    component_locations.append(car_location)
    component_posteds.append(car_posted)
    component_prices_eur.append(price_eur)
    component_prices_kn.append(price_kn)

    dict = {'Title': component_titles, 'Link': component_links, 'Type': component_types, 'Range': component_ranges, 'Year': component_years, 'Location': component_locations, 'Posted': component_posteds, 'Price EUR': component_prices_eur, 'Price KN': component_prices_kn}
    df = pd.DataFrame(dict)

    df.to_csv('Result.csv', index = False)
    
    
driver.get("https://www.njuskalo.hr/auti/c-max?page=2")
time.sleep(10)

totalbox = driver.find_element(By.XPATH, '//*[@id="form_browse_detailed_search"]/div/div[1]/div[7]/div[4]/ul')

subcategories = totalbox.find_elements(By.CLASS_NAME, "entity-body")

for i in range(len(subcategories)):
    title = subcategories[i].find_element(By.TAG_NAME, "h3").text
    # print("Title--> ", title)
    link = subcategories[i].find_element(By.CLASS_NAME, "entity-title").find_element(By.CLASS_NAME, "link").get_attribute("href")
    # print("LInk--> ", link)
    details = subcategories[i].find_element(By.CLASS_NAME, "entity-description-main").text

    ########## split details
    detail_elements = details.split("\n")

    type_range = detail_elements[0].split(",")
    car_type = type_range[0]
    car_range = type_range[1]
    # print("Type-->", car_type)
    # print("Range-->", car_range)

    car_year = detail_elements[1].split(":")[1].replace(".", "")
    # print("Year-->", car_year)

    car_location = detail_elements[2].split(":")[1]
    # print("Location-->", car_location)
    ########### split end

    times = subcategories[i].find_element(By.CLASS_NAME, "date--full").text
    car_posted = times.replace(".", "")
    # print("Posted-->", car_posted)

    price = subcategories[i].find_element(By.CLASS_NAME, "price--hrk").text
    price_eur = price.split("/")[0]
    price_kn = price.split("/")[1]
    # print("Price EUR-->", price_eur)
    # print("Price KN-->", price_kn)
    # print("-------------------------")

    # Open the CSV file in append mode
    with open('Result.csv', mode='a', newline='', encoding = 'utf-8') as file:
        writer = csv.writer(file)

        # Write the new row to the CSV file
        writer.writerow([title, link, car_type, car_range, car_year, car_location, car_posted, price_eur, price_kn])

    print('Data appended to CSV file.')