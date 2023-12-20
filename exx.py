#General TODOs for everywhere
#TODO: link all print functions to one UI function so that it could work with any front end
#TODO: consider if it would make more sense to just down load the entire json file and mine it directly
#TODO: standardize local/global variable convention, to avoid repeating variables or unintented linking
#============================================================================
# ||||||||||||||MAKE OUTPUT FOLDER
#============================================================================
# import the os module
import os

# get the current working directory
cwd = os.getcwd()

# get the name of the folder 'cellfiles'
folder_name = "cellfiles"

# check if the folder 'cellfiles' exists
if not os.path.exists(os.path.join(cwd, folder_name)):
    # create the folder 'cellfiles'
    os.makedirs(os.path.join(cwd, folder_name))
    # print a message
    print("Folder %s created!" % folder_name)
else:
    # print a message
    print("Folder %s already exists." % folder_name)


#============================================================================
#||||||||||||||ONLINE TO LOCAL STORAGE
# Getting the information from an online website onto local JSON files
# and putting them in the folder we created
#============================================================================
# -*- coding: utf-8 -*-
import pandas as pd
import glob
import urllib.request, json
import os # import the os module

#read the json file into a dataframe
url = "https://ccf-ontology.hubmapconsortium.org/v2.3.0/ccf-asctb-all.json"
with urllib.request.urlopen(url) as json_input:
    data = json.load(json_input)
df = pd.DataFrame(data)

#give all of the headers for the columns
headers = df.columns

# make all of the json files
for header in headers:
    data = df[header]['parsed']
    # create the path for your 'cellfiles' folder by joining it with its name
    cellfiles_path = os.path.join(os.getcwd(), "cellfiles")
    # create a full path for your file by joining it with its name and extension
    file_path = os.path.join(cellfiles_path, f"{header}.json")
    # open and write your file using the full path
    with open(file_path, 'w', encoding='utf-8') as f:
        # remove empty strings from each line of data
        data = [list(filter(None, line)) for line in data]
        json.dump(data, f, ensure_ascii=False, indent=4)

#%% start of extracting the relevant data
ALL_data_files = glob.glob('*.json')
for data_file in ALL_data_files:
    with open(data_file, 'r') as f:
        data = json.load(f)
        #print(data_file)
        #print(data)
print("Finished saving data locally")

#============================================================================
# |||||||||||||| DATAMINE
# Mine the relavant data from the big json file.
#============================================================================
#TODO: fix the datamining so that it does not only work for blood.

import json
import os # import the os module

# get the name of the folder 'cellfiles'
folder_name = "cellfiles"

# get a list of all the json files in the folder
json_files = [f for f in os.listdir(folder_name) if f.endswith(".json")]

# create an empty list to store the filtered data
filtered_data = []

# loop over each json file
for json_file in json_files:
    # create the path for your file by joining it with its name
    file_path = os.path.join(folder_name, json_file)
    # load the json file into a dictionary
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # extract only the "AS/1", "CT/1" and "All Gene Biomarkers" from each sublist
    for sublist in data[9:]:
        try:
            # try to access the elements at index 0, 3, and 9
            # append them to the filtered_data list
            filtered_data.append([sublist[0], sublist[3], sublist[9]])
        except IndexError:
            # catch the IndexError and print the message
            currentCol = str(sublist)
            print("Column not found in"+currentCol)
            # skip the current iteration and move on to the next sublist
            continue

# write the filtered_data list into a new json file
with open("filtered_compleate_celllist.json", "w") as f:
    json.dump(filtered_data, f, indent=4)

print("Finished mining the data")


#============================================================================
# |||||||||||||| MAKE WIKITABLE
# formats the mined data into a wikitable
#============================================================================
#TODO: format it into a sortable wikitable which is also collapsable or scrollable
#TODO: format it so that it is on the same format as the table on list of cells
#TODO: Make it go directly from JSON to wikitable.(try out updated code)
#TODO: include Biomarkers

import json

# Open the json file and load the data
with open("filtered_compleate_celllist.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

# Create a list of header names
headers = ["No.", "Name", "Progenitor(precursor cell)", "Predecessor Cells", "Location in Body", "Function", "Cell type", "Cell subtype", "Cell subtype", "Originally derived from", "Biomarkers"]

# Create a list of rows with the data from the json file
rows = []

# Loop over the data list using the index i
for i in range(len(data)):
    # Access the sublist using data[i]
    cell_type = data[i]

    # Create a row with the sublist elements
    row = [i+1, cell_type[0], "", "", cell_type[1], "", "", "", "","", ", ".join(cell_type[2])]

    # Append the row to the rows list
    rows.append(row)

# Open a text file and write the wikitable
with open("wikitable.txt", "w", encoding="utf-8") as text_file:
    text_file.write("""<templatestyles src="COVID-19 pandemic data/styles2.css" />
<div class="covid19-container"><div class="scroll-container">
{{Static row numbers}}""")
    text_file.write("\n{| class=\"wikitable sortable static-row-numbers\"\n")
    text_file.write("|-\n")
    text_file.write("|+ List Of all Human cells\n")
    for header in headers:
        text_file.write("! " + header + "\n")
    for row in rows:
        text_file.write("|-\n")
        for cell in row:
            text_file.write("| " + str(cell) + "\n")
    text_file.write("|}")
    text_file.write(""" </div></div>""")

# Close the text file
text_file.close()

#============================================================================
# |||||||||||||| MERGE WITH CURRENT WIKI TABLE
# Make a list of merge conflicts with current table on wikie
# Take hyperlinks from current WIKITABLE on wii
# Make a suggestion for what an updated wiki table could look like
#============================================================================
