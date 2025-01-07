import pandas as pd
import os
import numpy as np
from datetime import datetime
# import pyodbc     #Use for connecting to the server

#Start time for run time calc
startTime = datetime.now()

directory = "C:/Users/jtilsch/OneDrive - Pioneer Valley Planning Commission/Desktop/Python Data/Done 2023/"
NAICS = ["72", "56", "71", "23", "61", "52", "62", "51", "31-33","55", "81", "54", "53", "44-45", "48-49","22", "42", "10","92"]
Year = "2023"

Database_df_Headers = ['PAYROLL','PAYROLL_PRIVATE','AVGWEEKLYWAGE',
                       'ESTABLISHMENTS','ESTAB_MFG','EMPLOYMENT-WRKPLC','EMPLOYMENT_SELF','EMPLOYMENT_UTIL',
                       'EMPLOYMENT_CONST','EMPLOYMENT_MFG','EMPLOYMENT_Whole_TR','EMPLOYMENT_RET_TR',
                       'EMPLOYMENT_TRANS_WARE','EMPLOYMENT_INFO','EMPLOYMENT_FIN_INSUR','EMPLOYMENT_REAL_ESTATE',
                       'EMPLOYMENT_PROF_SCI_TECH','EMPLOYMENT_MGMT','EMPLOYMENT_ADMIN_WASTE','EMPLOYMENT_EDUC_SVCS',
                       'EMPLOYMENT_HEALTH_SOCIAL','EMPLOYMENT_ARTS_REC','EMPLOYMENT_ACCOM_FOOD','EMPLOYMENT_OTHER',
                       'EMPLOYMENT_GOVT','EMP_INDUSTRIES_TOT','EMPLOYMENT-WRKPLC_PERC','EMPLOYMENT_SELF_PERC',
                       'EMPLOYMENT_UTIL_PERC','EMPLOYMENT_CONST_PERC','EMPLOYMENT_MFG_PERC','EMPLOYMENT_Whole_TR_PERC',
                       'EMPLOYMENT_RET_TR_PERC','EMPLOYMENT_TRANS_WARE_PERC','EMPLOYMENT_INFO_PERC',
                       'EMPLOYMENT_FIN_INSUR_PERC','EMPLOYMENT_REAL_ESTATE_PERC','EMPLOYMENT_PROF_SCI_TECH_PERC',
                       'EMPLOYMENT_MGMT_PERC','EMPLOYMENT_ADMIN_WASTE_PERC','EMPLOYMENT_EDUC_SVCS_PERC',
                       'EMPLOYMENT_HEALTH_SOCIAL_PERC','EMPLOYMENT_ARTS_REC_PERC','EMPLOYMENT_ACCOM_FOOD_PERC',
                       'EMPLOYMENT_OTHER_PERC','EMPLOYMENT_GOVT_PERC','EMPLOY_1-4','EMPLOY_5-9','EMPLOY_10-19',
                       'EMPLOY_20-49','EMPLOY_50-99','EMPLOY_100-249','EMPLOY_250-499','EMPLOY_500+','RECENT_YEAR',
                       'HAVE_DATA','LAST_MODIFIED'
]

communities = ['Agawam','Amherst','Ashfield','Belchertown','Bernardston','Blandford','Brimfield','Buckland',
               'Charlemont','Chester','Chesterfield','Chicopee','Colrain','Conway','Cummington','Deerfield',
               'East Longmeadow','Easthampton','Erving','Franklin County','Gill','Goshen','Granby','Granville',
               'Greenfield','Hadley','Hampden County','Hampden','Hampshire County','Hatfield','Hawley','Heath','Holland',
               'Holyoke','Huntington','Leverett','Leyden','Longmeadow','Ludlow','Middlefield','Monroe','Monson','Montague',
               'Montgomery','New Salem','Northampton','Northfield','Orange','Palmer','Pelham','Plainfield',
               'PVPC Region', 'Pioneer Valley','Rowe','Russell','Shelburne','Shutesbury','South Hadley','Southampton',
               'Southwick','Springfield','Sunderland','Tolland','Wales','Ware','Warwick','Wendell','West Springfield',
               'Westfield','Westhampton','Whately','Wilbraham','Williamsburg','Worthington']

# shape = (73,62), instantiate this shape with NaN values to be spot replaced later and otherwise represent missing data
#Insert static values for Town, State, Time Type etc etc...
community_series = pd.Series(communities)
Database_df = pd.DataFrame(np.nan, index = range(len(communities)), columns = Database_df_Headers)
Database_df.insert(0, "YEAR", Year)
Database_df.insert(0, "TIME_VALUE", "...")
Database_df.insert(0, "TIME_TYPE", "Annual")
Database_df.insert(0, "COMMUNITY", communities)
Database_df.insert(0, "STATE", "MA")
#get the community column in the database df
check = Database_df['COMMUNITY'][0:65]

combined_df = pd.DataFrame()                                 #Create the empty dataframe container

for file in os.listdir(directory):
    file_path = os.path.join(directory, file)                #Join directory with file name to be able to access the contents
    if file.endswith(".csv"):
        df = pd.read_csv(file_path, on_bad_lines='skip')
        df = pd.read_csv(file_path,                          #Get the table and skip the meta data
                         skiprows=8,                         # This may need to be adjusted in order to get the program to run, make sure it brings  you to the top of the actual data table
                         engine='python',
                         skipfooter=3,
                         on_bad_lines='skip',
                         usecols =['NAICS', 'Description','No. of Establishments','Total Wages', 'Average Monthly Employment',
                                   'Average Weekly Wages'],
                         thousands=',')
        df['NAICS'] = df['NAICS'].astype(str).str.strip()
        df_filtered = df[df['NAICS'].isin(NAICS)]
        town_name = os.path.splitext(file)[0]
        # print(len(df_filtered['NAICS']))
        df_filtered.insert(0, "Community", town_name)       #insert a column for year and community to ID data
        df_filtered.insert(1, "Year", Year)
        # Concatenate all dataframes to a single dataframe
        combined_df = pd.concat([combined_df, df_filtered], ignore_index=True)

print(f'This is the combined Dataframe \n{combined_df.to_string()}')

filter_frame = combined_df[combined_df['NAICS'] == '10']
print(filter_frame.to_string())

#instantiate the sequence of NAICS codes we are going to use in the function
NAICS_Seq = ['10','10','10','31-33','10','22','23','31-33','42','44-45','48-49','51','52','53','54','55','56','61',
             '62','71','72','81','92']
#Instantiate the sequence of column names in the Database Dataframe to allocate to DB frame
DB_Cols = ['PAYROLL','AVGWEEKLYWAGE','ESTABLISHMENTS','ESTAB_MFG','EMPLOYMENT-WRKPLC','EMPLOYMENT_UTIL','EMPLOYMENT_CONST',
           'EMPLOYMENT_MFG','EMPLOYMENT_Whole_TR','EMPLOYMENT_RET_TR','EMPLOYMENT_TRANS_WARE','EMPLOYMENT_INFO',
           'EMPLOYMENT_FIN_INSUR','EMPLOYMENT_REAL_ESTATE','EMPLOYMENT_PROF_SCI_TECH','EMPLOYMENT_MGMT',
           'EMPLOYMENT_ADMIN_WASTE','EMPLOYMENT_EDUC_SVCS','EMPLOYMENT_HEALTH_SOCIAL','EMPLOYMENT_ARTS_REC',
           'EMPLOYMENT_ACCOM_FOOD','EMPLOYMENT_OTHER','EMPLOYMENT_GOVT','EMP_INDUSTRIES_TOT']

FLT_Cols = ['Total Wages','Average Weekly Wages','No. of Establishments','No. of Establishments',
            'Average Monthly Employment','Average Monthly Employment','Average Monthly Employment',
            'Average Monthly Employment','Average Monthly Employment','Average Monthly Employment',
            'Average Monthly Employment','Average Monthly Employment','Average Monthly Employment',
            'Average Monthly Employment','Average Monthly Employment','Average Monthly Employment',
            'Average Monthly Employment','Average Monthly Employment','Average Monthly Employment',
            'Average Monthly Employment','Average Monthly Employment','Average Monthly Employment',
            'Average Monthly Employment']

def non_calc_cols(Database_df, combined_df):
    for a, b, c in zip(NAICS_Seq, DB_Cols, FLT_Cols):
        filter_frame = combined_df[combined_df['NAICS'] == a]
        for i in Database_df.index:
            database_town = Database_df['COMMUNITY'][i]
            for j in filter_frame.index:
                filtered_town = filter_frame['Community'][j]
                if database_town == filtered_town:
                    Database_df.at[i, b] = filter_frame.at[j, c]
    return Database_df

x = non_calc_cols(Database_df, combined_df)

print(x.to_string())

#Python 3:
print(datetime.now() - startTime)



# check the data types for all columns, convert what ever is necessary to integer to do calcs on cal columns

type_convert = ['YEAR','ESTABLISHMENTS', 'ESTAB_MFG', 'EMPLOYMENT-WRKPLC',
                'EMPLOYMENT_SELF','EMPLOYMENT_UTIL','EMPLOYMENT_CONST','EMPLOYMENT_MFG','EMPLOYMENT_Whole_TR',
                'EMPLOYMENT_RET_TR','EMPLOYMENT_TRANS_WARE','EMPLOYMENT_INFO','EMPLOYMENT_FIN_INSUR','EMPLOYMENT_REAL_ESTATE',
                'EMPLOYMENT_PROF_SCI_TECH','EMPLOYMENT_MGMT','EMPLOYMENT_ADMIN_WASTE','EMPLOYMENT_EDUC_SVCS',
                'EMPLOYMENT_HEALTH_SOCIAL','EMPLOYMENT_ARTS_REC','EMPLOYMENT_ACCOM_FOOD','EMPLOYMENT_OTHER']

# Convert necessary columns into the correct data type, use float for now since it can handle ints too

WRKPLC = Database_df['EMPLOYMENT-WRKPLC'].replace({",":""}, regex = True)
print(WRKPLC.dtypes)
print(WRKPLC)
for i in type_convert:
    Database_df[i] = pd.to_numeric(Database_df[i], errors='coerce')

print(Database_df.dtypes.to_string())



non_calc = ['EMPLOYMENT_SELF','EMPLOYMENT_UTIL','EMPLOYMENT_CONST','EMPLOYMENT_MFG','EMPLOYMENT_Whole_TR',
                 'EMPLOYMENT_RET_TR','EMPLOYMENT_TRANS_WARE','EMPLOYMENT_INFO','EMPLOYMENT_FIN_INSUR',
                 'EMPLOYMENT_REAL_ESTATE','EMPLOYMENT_PROF_SCI_TECH','EMPLOYMENT_MGMT','EMPLOYMENT_ADMIN_WASTE',
                 'EMPLOYMENT_EDUC_SVCS','EMPLOYMENT_HEALTH_SOCIAL','EMPLOYMENT_ARTS_REC','EMPLOYMENT_ACCOM_FOOD',
                 'EMPLOYMENT_OTHER','EMPLOYMENT_GOVT'
                 ]

calc = ['EMPLOYMENT_SELF_PERC','EMPLOYMENT_UTIL_PERC','EMPLOYMENT_CONST_PERC',
             'EMPLOYMENT_MFG_PERC','EMPLOYMENT_Whole_TR_PERC','EMPLOYMENT_RET_TR_PERC','EMPLOYMENT_TRANS_WARE_PERC',
             'EMPLOYMENT_INFO_PERC','EMPLOYMENT_FIN_INSUR_PERC','EMPLOYMENT_REAL_ESTATE_PERC',
             'EMPLOYMENT_PROF_SCI_TECH_PERC','EMPLOYMENT_MGMT_PERC','EMPLOYMENT_ADMIN_WASTE_PERC',
             'EMPLOYMENT_EDUC_SVCS_PERC','EMPLOYMENT_HEALTH_SOCIAL_PERC','EMPLOYMENT_ARTS_REC_PERC',
             'EMPLOYMENT_ACCOM_FOOD_PERC','EMPLOYMENT_OTHER_PERC','EMPLOYMENT_GOVT_PERC'
]


for i, j in zip(non_calc, calc):
    print(i,j)
    Database_df[j] = Database_df[i] / Database_df['EMPLOYMENT-WRKPLC']

# Database_df['EMPLOYMENT-WRKPLC'] = WRKPLC

print(Database_df.to_string())

Database_df.to_csv('C:/Users/jtilsch/OneDrive - Pioneer Valley Planning Commission/Desktop/Python Data/Extract Wages_'+Year+'.csv')






