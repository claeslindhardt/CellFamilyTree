# Import json and csv modules
import json
import csv

# Open the json file and load the data
with open("cell_types.json", "r") as json_file:
  data = json.load(json_file)

# Create a list of header names
headers = ["No.", "Name", "Location", "Biomarkers"]

# Create a list of rows with the data from the json file
rows = []
for i, cell_type in enumerate(data["cell_types"], start=1):
  row = [i, cell_type["name"], cell_type["location"], ", ".join(cell_type["biomarkers"])]
  rows.append(row)

# Open a csv file and write the header and rows
with open("cell_types.csv", "w", newline="") as csv_file:
  writer = csv.writer(csv_file)
  writer.writerow(headers)
  writer.writerows(rows)

# Print the wikitable sortable static-row-numbers
print("{| class=\"wikitable sortable static-row-numbers\"")
print("|-")
for header in headers:
  print("! " + header)
for row in rows:
  print("|-")
  for cell in row:
    print("| " + str(cell))
print("|}")
