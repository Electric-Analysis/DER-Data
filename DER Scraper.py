#64 bit chrome
#Version 118.0.5993.71
# C:\Program Files (x86)
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import os
import glob
from selenium.webdriver.common.keys import Keys
import time
# from selenium.webdriver.common.by import By
########################################################################################################################
#STATIC VARIABLES AND LISTS

#Get path to chromedriver to execute commands through
PATH = "C:\Program Files (x86)\chromedriver.exe"

#Track run time, get a baseline time variable
GLOBAL_START_TIME = time.time()
items_done = 0
runtimes = []
sleep_timer = 3
YEAR = "2023"
#HTML objects to reference for web driving
# value_list = ["ddAreaType","ddSpecificArea","ddYearSelector","ddTimePeriod","ddOwnership","ddIndustry","lmi__radio",
#               "Download and save the data as a Comma Separated Value (CSV) file"]

# Towns to cycle through
communities = ['Agawam','Amherst','Ashfield','Belchertown','Bernardston','Blandford','Brimfield','Buckland',
               'Charlemont','Chester','Chesterfield','Chicopee','Colrain','Conway','Cummington','Deerfield',
               'East Longmeadow','Easthampton','Erving','Gill','Goshen','Granby','Granville',
               'Greenfield','Hadley','Hampden','Hatfield','Hawley','Heath','Holland','Holyoke','Huntington',
               'Leverett','Leyden','Longmeadow','Ludlow','Middlefield','Monroe','Monson','Montague',
               'Montgomery','New Salem','Northampton','Northfield','Orange','Palmer','Pelham','Plainfield',
               'Rowe','Russell','Shelburne','Shutesbury','South Hadley','Southampton','Southwick','Springfield',
               'Sunderland','Tolland','Wales','Ware','Warwick','Wendell','West Springfield','Westfield',
               'Westhampton','Whately','Wilbraham','Williamsburg','Worthington']

# Modify this list if you need to restart without redoing all the work again, remove from the second list what has been
# completed or skipped. DO NOT MODIFY THE ORIGINAL __^
# communities = ['Amherst','Ashfield','Belchertown','Bernardston','Blandford','Brimfield','Buckland',
#                'Charlemont','Chester','Chesterfield','Chicopee','Colrain','Conway','Cummington','Deerfield',
#                'East Longmeadow','Easthampton','Erving','Gill','Goshen','Granby','Granville',
#                'Greenfield','Hadley','Hampden','Hatfield','Hawley','Heath','Holland','Holyoke','Huntington',
#                'Leverett','Leyden','Longmeadow','Ludlow','Middlefield','Monroe','Monson','Montague',
#                'Montgomery','New Salem','Northampton','Northfield','Orange','Palmer','Pelham','Plainfield',
#                'Rowe','Russell','Shelburne','Shutesbury','South Hadley','Southampton','Southwick','Springfield',
#                'Sunderland','Tolland','Wales','Ware','Warwick','Wendell','West Springfield','Westfield',
#                'Westhampton','Whately','Wilbraham','Williamsburg','Worthington']

counties = ["Franklin County", "Hampden County","Hampshire County"]


########################################################################################################################
# Runtime function to track runtime, currently not in use. Develop later to cut down on wet code.
# def Runtime(items_done, runtimes, GLOBAL_START_TIME):
#     avg_runtime = len(runtimes)/sum(runtimes)
#     runtime = items_done*avg_runtime
#     remaining_time = (len(communities)-items_done)*avg_runtime
#     return remaining_time



#Function to crawl through webpage and select each option from the drop down menus and radio buttons. Automates the
#downloading of data into your downloads folder on the C drive.
def Community_Scraper(community,YEAR):
    #Implement run time tracking so we can watch what
    # stage what town etc and pin point failures more easily
    print("_______________________________")
    print(f'Time: {round((time.time()-GLOBAL_START_TIME)/60,4)} Minutes \nExecuting new selection: \n{community}')

    driver = webdriver.Chrome()
    driver.get("https://lmi.dua.eol.mass.gov/LMI/EmploymentAndWages#")

    while True:
        try:
            search = driver.find_element(by=By.ID, value="ddAreaType")
            select = Select(search)
            select.select_by_visible_text("City or Town")
            break
        except NoSuchElementException:
            print("Element does not exist, waiting a few seconds then trying again")
            print(round((time.time()-GLOBAL_START_TIME)/60,2))

    while True:
        try:
            search = driver.find_element(by=By.ID, value="ddSpecificArea")
            select = Select(search)
            select.select_by_visible_text(community)
            break
        except NoSuchElementException:
            print("Element does not exist, waiting a few seconds then trying again")
            print(round((time.time()-GLOBAL_START_TIME)/60,2))

    while True:
        try:
            time.sleep(sleep_timer)
            search = driver.find_element(by=By.ID, value="ddYearSelector")
            select = Select(search)
            select.select_by_visible_text(YEAR)
            break
        except NoSuchElementException:
            print("Element does not exist, waiting a few seconds then trying again")
            print(round((time.time()-GLOBAL_START_TIME)/60,2))

    while True:
        try:
            time.sleep(sleep_timer)
            search = driver.find_element(by=By.ID, value="ddTimePeriod")
            select = Select(search)
            select.select_by_visible_text("Annual Report")
            break
        except NoSuchElementException:
            print("Element does not exist, waiting a few seconds then trying again")
            print(round((time.time()-GLOBAL_START_TIME)/60,2))

    while True:
        try:
            time.sleep(sleep_timer)
            search = driver.find_element(by=By.ID, value="ddOwnership")
            select = Select(search)
            select.select_by_visible_text("All ownership types")
            break
        except NoSuchElementException:
            print("Element does not exist, waiting a few seconds then trying again")
            print(round((time.time()-GLOBAL_START_TIME)/60,2))

    while True:
        try:
            time.sleep(sleep_timer)
            search = driver.find_element(by=By.ID, value="ddIndustry")
            select = Select(search)
            select.select_by_visible_text("Total, All Industries")
            break
        except NoSuchElementException:
            print("Element does not exist, waiting a few seconds then trying again")
            print(round((time.time()-GLOBAL_START_TIME)/60,2))

#This currently selects the first radio button but we need the second one.
    link = driver.find_element(by=By.XPATH, value= '//*[@id="liCategory"]/div[3]/label[2]')
    link.click()

    link = driver.find_element(by=By.LINK_TEXT,
                               value="Download and save the data as a Comma Separated Value (CSV) file")
    link.click()

    time.sleep(sleep_timer)
    driver.quit()
    time.sleep(2)

def County_Scraper(county,YEAR):
    # Implement run time tracking so we can watch what
    # stage what town etc and pin point failures more easily
    n=0
    print("_______________________________")
    print(f'Time: {round((time.time() - GLOBAL_START_TIME) / 60,4)} Minutes \nExecuting new selection: \n{county}')

    driver = webdriver.Chrome()
    driver.get("https://lmi.dua.eol.mass.gov/LMI/EmploymentAndWages#")

    while True:
        try:
            search = driver.find_element(by=By.ID, value="ddAreaType")
            select = Select(search)
            select.select_by_visible_text("County")
            break
        except NoSuchElementException:
            print("Element does not exist, waiting a few seconds then trying again")
            print(round((time.time() - GLOBAL_START_TIME) / 60, 2))

    while True:
        try:
            search = driver.find_element(by=By.ID, value="ddSpecificArea")
            select = Select(search)
            select.select_by_visible_text(county)
            break
        except NoSuchElementException:
            print("Element does not exist, waiting a few seconds then trying again")
            print(round((time.time() - GLOBAL_START_TIME) / 60, 2))

    while True:
        try:
            time.sleep(sleep_timer)
            search = driver.find_element(by=By.ID, value="ddYearSelector")
            select = Select(search)
            select.select_by_visible_text(YEAR)
            break
        except NoSuchElementException:
            print("Element does not exist, waiting a few seconds then trying again")
            print(round((time.time() - GLOBAL_START_TIME) / 60, 2))

    while True:
        try:
            time.sleep(sleep_timer)
            search = driver.find_element(by=By.ID, value="ddTimePeriod")
            select = Select(search)
            select.select_by_visible_text("Annual Report")
            break
        except NoSuchElementException:
            print("Element does not exist, waiting a few seconds then trying again")
            print(round((time.time() - GLOBAL_START_TIME) / 60, 2))

    while True:
        try:
            time.sleep(sleep_timer)
            search = driver.find_element(by=By.ID, value="ddOwnership")
            select = Select(search)
            select.select_by_visible_text("All ownership types")
            break
        except NoSuchElementException:
            print("Element does not exist, waiting a few seconds then trying again")
            print(round((time.time() - GLOBAL_START_TIME) / 60, 2))

    while True:
        try:
            time.sleep(sleep_timer)
            search = driver.find_element(by=By.ID, value="ddIndustry")
            select = Select(search)
            select.select_by_visible_text("Total, All Industries")
            break
        except NoSuchElementException:
            print("Element does not exist, waiting a few seconds then trying again")
            print(round((time.time() - GLOBAL_START_TIME) / 60, 2))

    # This currently selects the first radio button but we need the second one.
    link = driver.find_element(by=By.XPATH, value='//*[@id="liCategory"]/div[3]/label[2]')
    link.click()

    link = driver.find_element(by=By.LINK_TEXT,
                               value="Download and save the data as a Comma Separated Value (CSV) file")
    link.click()

    time.sleep(sleep_timer)
    driver.quit()
    time.sleep(2)


for community in communities:
    Community_Scraper(community, YEAR)
    try:
        home = os.path.expanduser('~')
        path = os.path.join(home, 'Downloads')

        path_a = path + "/*"
        list_of_files = glob.glob(path_a)
        latest_file = max(list_of_files, key=os.path.getctime)

        new_file = os.path.join(path, community+".csv")
        print(latest_file)

        os.rename(latest_file, new_file)
        print(new_file)
    except FileExistsError:
        print("The file already exists, please rename manually")


for county in counties:
    County_Scraper(county, YEAR)
    try:
        home = os.path.expanduser('~')
        path = os.path.join(home, 'Downloads')

        path_a = path + "/*"
        list_of_files = glob.glob(path_a)
        latest_file = max(list_of_files, key=os.path.getctime)

        new_file = os.path.join(path, county+".csv")
        print(latest_file)

        os.rename(latest_file, new_file)
        print(new_file)
    except FileExistsError:
        print("The file already exists, please rename manually")