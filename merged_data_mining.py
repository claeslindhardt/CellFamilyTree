#General TODOs for everywhere
#TODO: link all print functions to one UI function so that it could work with any front end
#TODO: consider if it would make more sense to just down load the entire json file and mine it directly
#TODO: standardize local/global variable convention, to avoid repeating variables or unintented linking
#%%
#============================================================================
#||||||||||||||ONLINE TO LOCAL STORAGE
# Getting the information from an online website onto local JSON files
# and putting them in the folder we created
# Input: A web URL that returns a JSON file
# Output:  A locally stored JSON file from HUBmap
#============================================================================
#TODO: consider to make it delete the file if there is one already, or give it another name
# -*- coding: utf-8 -*-
import pandas as pd
import urllib.request, json

#read the json file into a dataframe
url = "https://ccf-ontology.hubmapconsortium.org/v2.3.0/ccf-asctb-all.json"
with urllib.request.urlopen(url) as json_input:
    data = json.load(json_input)
df = pd.DataFrame(data)

#give all of the headers for the columns
headers = df.columns

for_json = {}
# make all of the json files
for header in headers:
    data = df[header]['parsed']
    search = [row[0] for row in data]
    first_index = search.index("AS/1")
    for_json[header] = data[first_index:]
#%%
#============================================================================
# |||||||||||||| DATAMINING AND FILTERING
# Mine the relavant data from the big json file.
# Input: A locally stored JSON file from HUBmap
# Output: A locally stored JSON file with only the data relevant for wikipedia
#============================================================================
import json
import re

filtered_data = []
Gene_pattern = re.compile(r'^BGene/\d+$')
Protein_pattern = re.compile(r'BProtein/\d+$')
CT_pattern = re.compile(r'^CT/\d+$')
for key, data_set in for_json.items():
    try:     
        Gene_indicies = [index for index, value in enumerate(data_set[0]) if Gene_pattern.match(value)]
        Protein_indicies = [index for index, value in enumerate(data_set[0]) if Protein_pattern.match(value)]
        AS_index = data_set[0].index("AS/1")
        
        CT_indicies = [index for index, value in enumerate(data_set[0]) if CT_pattern.match(value)]
        CT_indicies = CT_indicies[-1:]
        
        for entry in data_set[1:]:
            temp = []
            biomarkers = []
            bioproteins = []
            temp.append(entry[AS_index])
            
            if len(Gene_indicies) >= 1:
                for idx in Gene_indicies:
                    if entry[idx] != "":
                        biomarkers.append(entry[idx])
                if len(biomarkers) != 0:
                    temp.append(biomarkers)
                else:
                    temp.append("")
            else:
                temp.append("")
                
            if entry[CT_indicies[-1]]:
                for idx in CT_indicies:
                    if entry[idx] != "":
                        temp.insert(0, entry[idx])
                        break
            else:
                temp.insert(0, "CT not in database")
            
            if temp[0] != "CT not in database" and "" not in temp[2:]:
                filtered_data.append(temp)
    
    except:
        print(f"could not process {key}")
sorted_data = sorted(filtered_data, key = lambda x: x[0])
# write the filtered_data list into a new json file
# with open("filtered_compleate_celllist.json", "w") as f:
#     json.dump(filtered_data, f, indent=4)

unique_list = []
for sub_list in sorted_data:
    if sub_list not in unique_list:
        unique_list.append(sub_list)


print("Finished mining the data")

#%%
#============================================================================
# |||||||||||||| READ IN THE CURRENT WIKIPEDIAA TABLE 
# Takes the wikipedia article as turns the current table into a pandas DataFrame
# Input: The current wikipeida URL for general article
# Output: A locally stored .json file with all of the entries ofh te curretn wikitable
#============================================================================

url = 'https://en.wikipedia.org/wiki/List_of_distinct_cell_types_in_the_adult_human_body'
# 3 is a magic nubmer here. Will not need to be changed as long as the current
# article does not cahnge structure. Have no idea hwo we can make it adaptable
df = pd.read_html(url, header=0)[3]

#saves locally to the device
df.to_json('current_wikitalbe.json')

#%%
#============================================================================
# |||||||||||||| MAKE WIKITABLE
# formats the mined data into a wikitable
# Input: A locally stored JSON file with only the data relevant for wikipedia
# Output: A .txt file with a wiki Markdown table of all the info from the Hubmap DB
#============================================================================
#TODO: find a way to make the scrollable function work even for long lists
#TODO: integrate the code for adding hyper link references, 
#TODO: make hyperlinks and wiki sources on the cells, locations and biomarkers for which it is available
#TODO: make sure that the list is sorted alfabetically
#TODO: every time there is more then 5000(or whatever the styles2.css have as an upper limit) entries start a new table 

data = unique_list

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
# Input: A Link to a wikipedia article, as well as a locally stored .txt file with a draft for a table with new data
# Output:  A list of differences, merge conflicts and a draft for a new updated table
#============================================================================

