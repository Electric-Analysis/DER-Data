This project is used to collect data from the DER website on the following URL
https://lmi.dua.eol.mass.gov/LMI/EmploymentAndWages#

This application requires a combination of user input, user observation, and multiple scripts running in a sequence. 
First we need to collect data with the DER Scraper. This script will occasionally fail due to certain web page elements
not existing. The script is not robust to handle these exceptions and will start looping uncontrollably and must be 
observed or you may ddos the government page. Immediately stop the program if this happens. You must physically sit and
watch for this as it may happen a couple times as a function of incomplete data existing for certain towns. Be sure
you understand how to terminate the program before executing. Additionally, you will need to install selenium in a virtual
environment, set your IDE to use that venv, and download the correct webdrivers for chrome otherwise the script will fail
as it can not drive/navigate on the webpage we want to scrape. My instance of this script has the webdriver saved 
here:"C:\Program Files (x86)\chromedriver.exe", your path may vary but should be stored in the x86. A quick youtube 
video will easily describe the process for getting this up and running but I will not detail it exhaustively here.

Design:

Run DER Scraper (This must be observed). This will open the DER page and do the click work of filling out all the drop
down menus for each town, then click the download data button at the bottom. Additionally, it will rename the file in 
your downloads folder. If you are running this on a new computer you will need to make this your own downloads directory.
When a failure occurs it is recommended that you create a duplicate of the list containing
the town allocations (communities) that skips the failed execution and includes all the towns thereafter. Initialize the
semi-duplicate list right after the first one. This will skip past to your current position in the workflow and you may 
resume scraping. (I strongly recommend you do not modify the original list). This script will loop through all the necessary
steps of downloading data as it steps through the list of towns. Near the end of the script it will rename the file
in your downloads folder. Monitor this. Occassionally, it may fail to name the file resulting in the default file name.
This is not a big deal but you will need to figure out why, usually its because there is a file by the same name already,
just delete the other one and rename the file manually, if you arent sure, check the contents and rename to the name inside
the file. Once you have looped through all the towns it will repeat for the counties. If you run into any similar issues
described follow the same routine for counties. Once the script has finished running you will take all these files and 
put them into the directory for the next script to run. If you need multiple years you can indicate the year by changing 
the variable year in the code. Be sure to follow the directory structure that will be described next so that the data
extraction can work correctly.

Recommended File Structure for storing DER Data:

Python Data(
    Done 2001
    Done 2002
    Done 2003
    ...
    Done 2023
    Extracted Wages
    Misc
    To be dealt with)

This directory will allow you to store each year of data scraped in an organized
way so that you don't mix the vintages up which is very possible in this process. 
It is recommended that the data be copied and pasted into the respective folder relative
to the vintage. Although it's not yet "done" being worked on it is done being extracted. 
After each year
is scraped completely, the Employment Data Extraction script is intended to be used before 
collecting the next year. The output of that script will dump the completely concatenated 
file containing all the towns for the given year in the format for our database into a receiving file
named extracted wages
where all the completed years will accumulate. Once you have all the years in one place it is expected 
that you will pull them all into one file with excel. Be sure to append them to the database data
don't just update the table with the newest data. Be sure to modify 2 variables each time you run the
Employment Data Extraction script. directory, this must be changed to reflect the path that contains
your data in it. For me it was a matter of changing the number at the end of the path to the 
relevant year. Additionally, Year needs to be matched with the correct vintage otherwise the dataframe
that is output will indicate the wrong year. If you are running this on a different computer you may have
to either recreate my file structure or use your own but be mindful that you will have 3 variables to change
Year, Directory, and the Database_df.to_csv path







