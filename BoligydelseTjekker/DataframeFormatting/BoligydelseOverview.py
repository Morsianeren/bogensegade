#This script is used to create an neat overview of the boligydelse data.

import pandas as pd
import os

def BoligydelseOverview(boligydelser: pd.DataFrame) -> None:
    # First sort the data by 'Id'
    grouped = boligydelser.groupby('Id')

    #dfs = {category: group.reset_index(drop=True) for category, group in grouped}

    # Create an excel file to store the data
    output_excel_file = 'BoligydelseOverview.xlsx'
    output_excel_file = os.path.join(os.getcwd(), output_excel_file)

    with pd.ExcelWriter(output_excel_file, engine='openpyxl') as writer:
        for category, group in grouped:
            # Sort by date
            group = group.sort_values(by='Bogføringsdato', ascending=False)
            group.to_excel(writer, sheet_name=f'{category}', index=False, float_format="%.2f")

