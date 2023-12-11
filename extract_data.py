# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 22:41:05 2023

@author: MasKl
"""

import pandas as pd
import glob

#read the json file into a dataframe
with open('ccf-asctb-all.json', 'r') as json_input:
    df = pd.read_json(json_input)
#give all of the headers for the columns
headers = df.columns

# make all of the csv files
for header in headers:
    data = df[header]['parsed']
    with open(f'{header}.csv', 'w', encoding="utf-8") as f:
        for line in data[9:]:
            for entry in line:
                    f.write(f'{entry},')
            f.write('\n')

#%% start of extracting the relevant data
ALL_data_files = glob.glob('*.csv')
for data_file in ALL_data_files:
    with open(data_file, 'r') as f:
        headers = f.readline()
        print(data_file)
        print(headers)