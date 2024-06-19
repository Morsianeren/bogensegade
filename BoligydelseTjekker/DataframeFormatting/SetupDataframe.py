import pandas as pd
import os
import json
from typing import Iterable

CSV_KONTOBESKEDER_COLUMN = 'Beskrivelse'  # Name of the column in the CSV file
CSV_MONEY_COLUMN = 'Beløb'  # Name of the column in the CSV file

def SetupDataframe(json_path: str, csv_path: str) -> pd.DataFrame:
    json_data = ReadJsonFile(json_path)
    csv_data = ReadCsvFile(csv_path)

    # Dataframe to store payments with 'Kontobeskeder' in the CSV
    df = pd.DataFrame()

    # Check for 'Kontobeskeder' in JSON data
    for entry in JsonEntryGenerator(json_data):
        kontobeskeder = entry.get('Kontobeskeder')
        for besked in kontobeskeder:
            if besked in csv_data[CSV_KONTOBESKEDER_COLUMN].values:
                # Append the row to the dataframe
                rows = csv_data[csv_data[CSV_KONTOBESKEDER_COLUMN] == besked].copy()
                rows['Id'] = entry.get('Id')
                df = pd.concat([df, rows], ignore_index=True)

                # Remove the row from the CSV data
                csv_data = csv_data[csv_data[CSV_KONTOBESKEDER_COLUMN] != besked]

    return df

def ReadJsonFile(json_path: str, encoding: str = 'UTF-8') -> list:
    # Read JSON file
    with open(json_path, 'r', encoding=encoding) as json_file:
        json_data = json.load(json_file)
    return json_data

def ReadCsvFile(csv_path: str, delimiter:str=';', encoding:str='utf-8-SIG') -> pd.DataFrame:
    # Read CSV file
    csv_data = pd.read_csv(csv_path, delimiter=delimiter, encoding=encoding)
    return csv_data

def JsonEntryGenerator(json_data) -> Iterable[dict]:
    for entry in json_data:
        kontobeskeder = entry.get('Kontobeskeder', '').strip().split(';')
        entry['Kontobeskeder'] = kontobeskeder
        yield entry