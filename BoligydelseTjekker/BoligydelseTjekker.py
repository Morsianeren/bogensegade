import pandas as pd
import os
import json

# Define file paths
json_file_path = 'apartment_info.json'  # Path to the JSON file
csv_file_path = 'Driftskonto m noter.csv'    # Path to the CSV file
CSV_KONTOBESKEDER_COLUMN = 'Beskrivelse'  # Name of the column in the CSV file
CSV_MONEY_COLUMN = 'Beløb'  # Name of the column in the CSV file

csv_file_path = os.path.join(os.getcwd(), csv_file_path)
json_file_path = os.path.join(os.getcwd(), json_file_path)

# Read JSON file
with open(json_file_path, 'r', encoding='utf-8') as json_file:
    json_data = json.load(json_file)

# Read CSV file
csv_data = pd.read_csv(csv_file_path, delimiter=';', encoding='utf-8-SIG')

# Extract 'Kontobeskeder' from CSV
csv_kontobeskeder = csv_data[CSV_KONTOBESKEDER_COLUMN].astype(str).str.strip().tolist()

# Initialize a dataframe to store data that has 'Kontobeskeder' in the CSV

df = pd.DataFrame()

# Check for 'Kontobeskeder' in JSON data
for entry in json_data:
    kontobeskeder = entry.get('Kontobeskeder', '').strip()
    # Explode kontobeskeder using ';' as a delimiter
    kontobeskeder_list = kontobeskeder.split(';')
    for besked in kontobeskeder_list:
        if besked in csv_data[CSV_KONTOBESKEDER_COLUMN].values:
            # Prepare important data
            id = entry.get('id')

            # Append the row to the dataframe
            rows = csv_data[csv_data[CSV_KONTOBESKEDER_COLUMN] == besked].copy()
            rows['Id'] = id
            df = pd.concat([df, rows], ignore_index=True)

            #print(f"Found match for {besked} in JSON data with ID {id}")

            # Remove the row from the CSV data
            csv_data = csv_data[csv_data[CSV_KONTOBESKEDER_COLUMN] != besked]
