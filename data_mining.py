# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 18:43:52 2023

@author: MasKl
"""

import pandas as pd
import glob
import re

#read the json file into a dataframe
with open('ccf-asctb-all.json', 'r') as json_input:
    df = pd.read_json(json_input)
#give all of the headers for the columns
headers = df.columns

for_json = {}
# make all of the csv files
for header in headers:
    data = df[header]['parsed']
    search = [row[0] for row in data]
    first_index = search.index("AS/1")
    for_json[header] = data[first_index:]
    # with open(f'{header}.txt', 'w', encoding="utf-8") as f:
    #     for row in data[first_index:]:
    #         for entry in row:
    #             f.write(f'{entry} \t')
    #         f.write('\n')
    #     f.close()
#%%
filtered_data = {}
Gene_pattern = re.compile(r'^BGene/\d+$')
CT_pattern = re.compile(r'^CT/\d+$')
for key, data_set in for_json.items():
    try:
        data_indicies = [index for index, value in enumerate(data_set[0]) if Gene_pattern.match(value)]
        AS_index = data_set[0].index("AS/1")
        
        CT_indicies = [index for index, value in enumerate(data_set[0]) if CT_pattern.match(value)]
        CT_indicies = CT_indicies[-1:]
        
        fil_data = []
        for entry in data_set[1:]:
            temp = []
            biomarkers = []
            temp.append(entry[AS_index])
            for idx in data_indicies:
                if entry[idx] != "":
                    biomarkers.append(entry[idx])
            temp.append(biomarkers)
            for idx in CT_indicies:
                if entry[idx] != "":
                    temp.insert(1, entry[idx])
                    break
            fil_data.append(temp)
        filtered_data[key] = fil_data
    except:
        print(f"could not process {key}")
#%%
headers = ['AS', 'CT', 'Biomarkers']

with open("wikitable.txt", "w", encoding="utf-8") as text_file:
    text_file.write("{| class=\"wikitable sortable static-row-numbers\"\n")
    text_file.write("|-\n")
    for header in headers:
        text_file.write("! " + header + "\n")
    for key, values in filtered_data.items():
        for row in values:
            text_file.write("|-\n")
            text_file.write(f'| {row[0]} | {row[1]} |')
            if len(row) >= 3:
                for entry in row[2:]:
                    text_file.write(f'{entry}, ')
            text_file.write("\n")
    text_file.write("|}")

#%%
with open("filtered_data_2.csv", 'w') as f:
    f.write("AS, CT, BGENE, \n")
    for key, values in filtered_data.items():
        for row in values:
            for entry in row:
                f.write(f"{entry},")
            f.write('\n')
#%% start of extracting the relevant data
ALL_data_files = glob.glob('*.csv')
for data_file in ALL_data_files:
    with open(data_file, 'r') as f:
        headers = f.readline()
        print(data_file)
        print(headers)