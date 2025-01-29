import pandas as pd
import os
import numpy as np
from datetime import datetime


YEAR = 2024
directory = "C:/Users/jtilsch/OneDrive - Pioneer Valley Planning Commission/Desktop/Python Data/Laborforce and Employment/"+str(YEAR)+"/"

dataframes = []
for file in os.listdir(directory):
    file_path = os.path.join(directory, file)                #Join directory with file name to be able to access the contents
    # print(file_path)
    if file.endswith(".csv"):
        df = pd.read_csv(file_path, on_bad_lines='skip')
        df = pd.read_csv(file_path,                          #Get the table and skip the meta data
                         skiprows=6,                         # This may need to be adjusted in order to get the program to run, make sure it brings  you to the top of the actual data table
                         engine='python',
                         skipfooter=5,
                         # on_bad_lines='skip',
                         # usecols =['NAICS', 'Description','No. of Establishments','Total Wages', 'Average Monthly Employment',
                         #           'Average Weekly Wages'],
                         thousands=',')
        # print(df.to_string())
        df = df.drop(df.columns[6:9], axis=1)
        # df = df.drop([1, 11], axis=0)
        print(df.to_string())
        dataframes.append(df)

final_dataframe = pd.concat(dataframes, ignore_index = True)


print(final_dataframe.to_string())

Final_Dataframe = final_dataframe[final_dataframe.iloc[:, 2].str.contains("Annual", na=False)]

print(Final_Dataframe.to_string())

Final_Dataframe.to_csv('C:/Users/jtilsch/OneDrive - Pioneer Valley Planning Commission/Desktop/Python Data/Laborforce and Employment/Laborforce Concatenated Files/Concatenated Laborforce Data '+str(YEAR)+'.csv')

