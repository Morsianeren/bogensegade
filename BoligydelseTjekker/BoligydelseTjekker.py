import pandas as pd
import os
import json
from DataframeFormatting.SetupDataframe import SetupDataframe, ReadJsonFile
from DataframeFormatting.BoligydelseOverview import BoligydelseOverview

# Define file paths
json_file_path = 'apartment_info.json'  # Path to the JSON file
csv_file_path = 'Driftskonto m noter.csv'    # Path to the CSV file
CSV_KONTOBESKEDER_COLUMN = 'Beskrivelse'  # Name of the column in the CSV file
CSV_MONEY_COLUMN = 'Beløb'  # Name of the column in the CSV file

csv_file_path = os.path.join(os.getcwd(), csv_file_path)
json_file_path = os.path.join(os.getcwd(), json_file_path)


# First get the payments
boligydelser = SetupDataframe(json_file_path, csv_file_path)
json_data = ReadJsonFile(json_file_path)

# Next make it more visually appealing
BoligydelseOverview(boligydelser)