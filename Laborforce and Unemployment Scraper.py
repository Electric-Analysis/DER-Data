#64 bit chrome
#Version 118.0.5993.71
# C:\Program Files (x86)
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
sleep_timer = 1.5
YEAR = "2024"
#HTML objects to reference for web driving
# value_list = ["ddAreaType","ddSpecificArea","ddYearSelector","ddTimePeriod","ddOwnership","ddIndustry","lmi__radio",
#               "Download and save the data as a Comma Separated Value (CSV) file"]

def rename_latest_file(town, year):
    try:
        # Get the user's Downloads directory
        home = os.path.expanduser('~')
        downloads_path = os.path.join(home, 'Downloads')

        # Get the latest downloaded file
        list_of_files = glob.glob(os.path.join(downloads_path, "*"))
        latest_file = max(list_of_files, key=os.path.getctime)

        # Create the new file name
        new_file_name = f"{town} {year}.csv"
        new_file_path = os.path.join(downloads_path, new_file_name)

        # Check if a file with the new name already exists
        if os.path.exists(new_file_path):
            print(f"The file '{new_file_name}' already exists. Skipping rename.")
            return

        # Rename the file
        os.rename(latest_file, new_file_path)
        print(f"File renamed to: {new_file_path}")

    except FileExistsError:
        print(f"File already exists: {new_file_name}")
    except ValueError:
        print("No files found in the Downloads directory.")
    except Exception as e:
        print(f"An error occurred: {e}")


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

# communities = ['Palmer','Pelham','Plainfield',
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
    driver.get("https://lmi.dua.eol.mass.gov/lmi/LaborForceAndUnemployment?_ga=2.48249698.579691301.1737640022-132128474.1680878185#")

    while True:
        try:
            search = driver.find_element(By.XPATH, value='/html/body/div[1]/main/section/div/div/div/section/ol/li[1]/div[3]/select')
            select = Select(search)
            select.select_by_value("05")
            time.sleep(sleep_timer)
            break
        except NoSuchElementException:
            print("Element does not exist, waiting a few seconds then trying again")
            print(round((time.time()-GLOBAL_START_TIME)/60,2))
    while True:
        try:
            search = driver.find_element(By.XPATH, value='//*[@id="citySelector"]')
            select = Select(search)
            select.select_by_visible_text(community)
            print(f"Found: {community}")
            time.sleep(sleep_timer)
            break

        except NoSuchElementException:
            print("Element does not exist, waiting a few seconds then trying again")
            print(round((time.time() - GLOBAL_START_TIME) / 60, 2))

    while True:
        try:
            link = driver.find_element(by=By.XPATH,value= '/html/body/div[1]/main/section/div/div/div/section/ol/li[2]/div[4]/p/a')
            link.click()
            time.sleep(sleep_timer)
            break
        except NoSuchElementException:
            print("Element does not exist, waiting a few seconds then trying again")
            print(round((time.time()-GLOBAL_START_TIME)/60,2))

    while True:
        try:
            search = driver.find_element(By.NAME, value='ddTimePeriod')
            select = Select(search)
            select.select_by_value("3")
            search = driver.find_element(By.ID, value='yearSelector')
            select = Select(search)
            select.select_by_value(str(YEAR))
            link = driver.find_element(by=By.XPATH,value='/html/body/div[1]/main/section/div/div/div/section/ol/li[3]/div[3]/div[2]/p/a')
            link.click()
            time.sleep(sleep_timer)
            link = driver.find_element(by=By.XPATH,value='/html/body/div[1]/main/section/div/div/div/section/div[2]/div[2]/p[2]/a')
            link.click()
            print("Downloading Data")
            time.sleep(sleep_timer*3)

            break
        except NoSuchElementException:
            print("Element does not exist, waiting a few seconds then trying again")
            print(round((time.time()-GLOBAL_START_TIME)/60,2))





for town in communities:
    Community_Scraper(town, YEAR)
    print(f"Waiting for download: {sleep_timer*2.5}")
    time.sleep(sleep_timer * 1.3)
    try:
        home = os.path.expanduser('~')
        path = os.path.join(home, 'Downloads')

        path_a = path + "/*"
        list_of_files = glob.glob(path_a)
        latest_file = f"{path}\LURReport.csv"
        # "C:\Users\jtilsch\Downloads\LURReport.csv"
        new_file = os.path.join(path, f"{town} { YEAR}.csv")
        print(latest_file)

        os.rename(latest_file, new_file)
        print(new_file)
    except FileExistsError:
        print("The file already exists, please rename manually")
    # rename_latest_file(town, YEAR)




