#General TODOs for everywhere
#TODO: consider if it would make more sense to just down load the entire json file and mine it directly
#TODO: standardize local/global variable convention, to avoid repeating variables or unintented linking
#%%

#============================================================================
#||||||||||||||UI function
# Gathring all the input and output needed from the user in one place

class UIFunction:
    def downloadFinished(self):
        print("Finished downloading JSON data from HUBmap")

    def finishedMining(self):
        print("Finished mining the data")

    def processKeyExep(self):
        print(f"could not process {key}")

# Initialize class:
ui = UIFunction()

#%%

#============================================================================
#||||||||||||||ONLINE TO LOCAL STORAGE
# Getting the information from an online website onto local JSON files
# and putting them in the folder we created
# Input: A web URL that returns a JSON file
# Output:  A locally storeable JSON object from HUBmap
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

ui.downloadFinished()

'''
#To store the JSON object localy as a json file for debugging comment in this code
# Save the JSON object to a file
with open('data.json', 'w') as json_output:
    json.dump(for_json, json_output, indent=4)
'''


#%%
#============================================================================
# |||||||||||||| DATAMINING AND FILTERING
# Mine the relavant data from the big json file.
# Input: A locally stored JSON file from HUBmap
# Output: A locally storeable JSON object with only the data relevant for the wikipedia artilce on HUMAN CELLS
#============================================================================
import json
import re

filtered_data = []
'''
Ideally the following would be split into 2 functions
func 1: Data Mining:
Extracts relevant data: The code retrieves specific types of information from the input data:
Gene names matching the "BGene/\d+" pattern
Protein names matching the "BProtein/\d+" pattern
Cell type names matching the "CT/\d+" pattern

func 2 Filtering:
Applies multiple criteria: It filters the data based on various conditions:
The presence of a valid cell type (CT) entry
The presence of gene biomarkers
The absence of empty values in specific fields
'''

#The main potential issues with the way we use Try/catch
#Blanket except: The except: clause catches all exceptions, including those unrelated to the intended error handling.
#This can mask other potential issues in the code, making debugging more difficult.

#Unclear Error Handling: The except block calls ui.processKeyExep(),
#but it's unclear what this function does or how it addresses the specific errors.
#It's essential to have a clear understanding of how errors are managed to ensure the code's integrity.

#Potential for Missing Data: While the try-except block prevents the code from crashing,
#it might still miss or overlook certain data if errors occur. For example, if data_set[0] is empty,
#the indices will not be extracted correctly, leading to potential issues in subsequent processing.
#TODO: Resolve the above issues


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
        ui.processKeyExep()


#Sorts filtered data: The code arranges the filtered entries alphabetically based on the cell type (CT) value.
sorted_data = sorted(filtered_data, key = lambda x: x[0])

'''
# write the filtered_data list into a new json file
with open("filtered_celllist_sorted.json", "w") as f:
    json.dump(sorted_data, f, indent=4)
'''

#Removes duplicates: It eliminates redundant entries to produce a set of unique results.
unique_list = []
for sub_list in sorted_data:
    if sub_list not in unique_list:
        unique_list.append(sub_list)


'''
# write the unique_list list into a new json file
with open("filtered__celllist_noDublicates.json", "w") as f:
     json.dump(unique_list, f, indent=4)
'''

# Format the extracted data to fit the wiki table json format:

import json

def transform_json(input_json):
    """
    Transforms input JSON into the desired format.

    Args:
        input_json (list): Input JSON in the given format.

    Returns:
        dict: Transformed dictionary in the desired format.
    """
    transformed_dict = {
        "Name": {},
        "Progenitor (precursor cell)": {},
        "Predecessor Cells": {},
        "Location in Body": {},
        "Function": {},
        "Cell type": {},
        "Cell subtype": {},
        "Originally derived from": {},
        "Known biomarkers": {}
    }

    for idx, item in enumerate(input_json):
        name, location, biomarkers = item
        transformed_dict["Name"][str(idx)] = name
        transformed_dict["Location in Body"][str(idx)] = location
        transformed_dict["Known biomarkers"][str(idx)] = ", ".join(biomarkers) if biomarkers else None

    return transformed_dict

transformed_result = transform_json(unique_list)
with open("Transformed__celllist.json", "w") as f:
     json.dump(transformed_result, f, indent=4)


ui.finishedMining()

#%%

#============================================================================
# |||||||||||||| READ IN THE CURRENT WIKIPEDIAA TABLE
# Takes the wikipedia article as turns the current table into a pandas DataFrame
# Input: The current wikipeida URL for general article
# Output: A locally stored .json file with all of the entries ofh te curretn wikitable
#============================================================================
#Todo: find a way to also read in the hyperlinks on all the enteries.

url = 'https://en.wikipedia.org/wiki/List_of_distinct_cell_types_in_the_adult_human_body'
# 3 is a magic nubmer here. Will not need to be changed as long as the current
# article does not cahnge structure. Have no idea hwo we can make it adaptable
df = pd.read_html(url, header=0)[3]

#saves locally to the device
df.to_json('current_wikitalbe.json')


#%%
#============================================================================
# |||||||||||||| MERGE WITH CURRENT WIKI TABLE
# Make a list of merge conflicts with current table on wikie
# Take hyperlinks from current WIKITABLE on wii
# Make a suggestion for what an updated wiki table could look like
# Input: A Link to a wikipedia article, as well as a locally stored .txt file with a draft for a table with new data
# Output:  A list of differences, merge conflicts and a draft for a new updated table
#============================================================================



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

# Turn our json object back into a wiki table in a .txt file
import json

# Read JSON data from a file
with open('current_wikitalbe.json', 'r') as file:
    data = json.load(file)


# Function to convert 'null' to 'unknown'
def convert_null(value):
    return 'unknown' if value is None else value

# Function to create the table row
def create_row(index, data):
    return f"|-  \n |{data['Name'][str(index)]} \n | {convert_null(data['Progenitor (precursor cell)'][str(index)])} \n | {convert_null(data['Predecessor Cells'][str(index)])} \n | {data['Location in Body'][str(index)]} \n | {data['Function'][str(index)]} \n | {data['Cell type'][str(index)]} \n | {convert_null(data['Cell subtype'][str(index)])}\n  | {data['Originally derived from'][str(index)]} \n | {convert_null(data['Known biomarkers'][str(index)])} \n"

# Function to generate the table
def generate_table(data):
    table_header = '''<templatestyles src="COVID-19 pandemic data/styles2.css" />
<div class="covid19-container">
  <div class="scroll-container">
    {{Static row numbers}}
    {| class="wikitable sortable static-row-numbers"
    |-
    |+ List Of all Human cells
    ! Name
    ! Progenitor(precursor cell)
    ! Predecessor Cells
    ! Location in Body
    ! Function
    ! Cell type
    ! Cell subtype
    ! Originally derived from
    ! Biomarkers
    '''
    table_rows = ''
    for index in data['Name']:
        table_rows += create_row(index, data)

    table_footer = '''|}
  </div>
</div>'''

    return table_header + table_rows + table_footer

# Generate the table and write to a file
table_content = generate_table(data)
with open('human_cells_table.txt', 'w') as file:
    file.write(table_content)

#todo: add this to the UI class
print('The table has been written to human_cells_table.txt')


'''
data = unique_list

# Create a list of header names
headers = ["No.", "Name", "Progenitor(precursor cell)", "Predecessor Cells", "Location in Body", "Function", "Cell type", "Cell subtype", "Cell subtype", "Originally derived from", "Biomarkers"]

# Create a list of rows with the data from the json file
data = unique_list  # Your existing list of data

# Updated list of header names without "No." and one "Cell subtype"
headers = ["Name", "Progenitor(precursor cell)", "Predecessor Cells", "Location in Body", "Function", "Cell type", "Cell subtype", "Originally derived from", "Biomarkers"]

# Initialize the list of rows
rows = []

# Loop over the data list using the index i
for i in range(len(data)):
    cell_type = data[i]  # Access the sublist using data[i]
    # Create a row with the sublist elements, excluding "No." and one "Cell subtype"
    row = [cell_type[0], "", "", cell_type[1], "", "", "", "", ", ".join(cell_type[2])]
    rows.append(row)  # Append the row to the rows list

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
'''


#%%
