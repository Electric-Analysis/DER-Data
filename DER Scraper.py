#64 bit chrome
#Version 118.0.5993.71
# C:\Program Files (x86)
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
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



########################################################################################################################
# Runtime function to track runtime, currently not in use. Develop later to cut down on wet code.
# def Runtime(items_done, runtimes, GLOBAL_START_TIME):
#     avg_runtime = len(runtimes)/sum(runtimes)
#     runtime = items_done*avg_runtime
#     remaining_time = (len(communities)-items_done)*avg_runtime
#     return remaining_time



#Function to crawl through webpage and select each option from the drop down menus and radio buttons. Automates the
#downloading of data into your downloads folder on the C drive.
def Gov_Scraper(community):
    #Implement run time tracking so we can watch what
    # stage what town etc and pin point failures more easily
    print("_______________________________")
    print(f'Time: {(time.time()-GLOBAL_START_TIME)/60} Minutes \nExecuting new selection: \n{community}')

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
            time.sleep(7)
            search = driver.find_element(by=By.ID, value="ddYearSelector")
            select = Select(search)
            select.select_by_visible_text("2020")
            break
        except NoSuchElementException:
            print("Element does not exist, waiting a few seconds then trying again")
            print(round((time.time()-GLOBAL_START_TIME)/60,2))

    while True:
        try:
            time.sleep(7)
            search = driver.find_element(by=By.ID, value="ddTimePeriod")
            select = Select(search)
            select.select_by_visible_text("Annual Report")
            break
        except NoSuchElementException:
            print("Element does not exist, waiting a few seconds then trying again")
            print(round((time.time()-GLOBAL_START_TIME)/60,2))

    while True:
        try:
            time.sleep(7)
            search = driver.find_element(by=By.ID, value="ddOwnership")
            select = Select(search)
            select.select_by_visible_text("All ownership types")
            break
        except NoSuchElementException:
            print("Element does not exist, waiting a few seconds then trying again")
            print(round((time.time()-GLOBAL_START_TIME)/60,2))

    while True:
        try:
            time.sleep(7)
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

    print(f'{community} Runtime: {round(time.time()-GLOBAL_START_TIME,2)}\n')
    completion = (len(communities)-communities.index(community))*(time.time()-GLOBAL_START_TIME)/60
    print(f'Estimated remaining wait time:{round(completion,2)} Minutes')
    time.sleep(15)
    driver.quit()
    time.sleep(2)

for community in communities:
    Gov_Scraper(community)
