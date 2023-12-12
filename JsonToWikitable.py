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

# Open a text file and write the wikitable
with open("wikitable.txt", "w") as text_file:
  text_file.write("{| class=\"wikitable sortable static-row-numbers\"\n")
  text_file.write("|-\n")
  for header in headers:
    text_file.write("! " + header + "\n")
  for row in rows:
    text_file.write("|-\n")
    for cell in row:
      text_file.write("| " + str(cell) + "\n")
  text_file.write("|}")

# Close the text file
text_file.close()

