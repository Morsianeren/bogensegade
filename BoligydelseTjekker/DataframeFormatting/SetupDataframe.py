import pandas as pd
import copy
import json
from typing import Iterable

CSV_MESSAGE_COLUMN = 'Beskrivelse'  # Name of the column in the CSV file
CSV_MONEY_COLUMN = 'Beløb'  # Name of the column in the CSV file
CSV_NOTES_COLUMN = 'Noter'
CSV_SUBJECT_COLUMN = 'Emne'
CSV_SUBJECT_TEXT = 'Boligydelse' # The text to look for in the 'Emne' column

JSON_ID_COLUMN = 'Id'
JSON_MESSAGE_COLUMN = 'Kontobeskeder'

def SetupDataframe(json_path: str, csv_path: str) -> pd.DataFrame:
    json_data = ReadJsonFile(json_path)
    csv_data = ReadCsvFile(csv_path)

    # Dataframe to store payments with 'Kontobeskeder' in the CSV
    df = pd.DataFrame(columns=csv_data.columns.tolist() + [JSON_ID_COLUMN])

    # Check for 'Kontobeskeder' in JSON data
    GetPaymentsByMessage(df, csv_data, json_data)

    # Check if there are any unprocessed payments
    unprocessed_data = GetUnprocessedPayments(csv_data)
    if unprocessed_data.empty:
        return df

    # Check for payments using notes in the CSV
    GetPaymentsByNotes(df, csv_data, json_data)

    # Check for unprocessed payments
    unprocessed_data = GetUnprocessedPayments(csv_data)
    if not unprocessed_data.empty:
        # Write the unprocessed data to a new CSV file
        print("Unprocessed payments found. Writing to 'UnprocessedPayments.csv'...")
        unprocessed_data.to_csv('UnprocessedPayments.csv', index=False)

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

def GetPaymentsByMessage(target_df:pd.DataFrame, csv_data: pd.DataFrame, json_data) -> None:
    for entry in JsonEntryGenerator(json_data):
        kontobeskeder = entry.get(JSON_MESSAGE_COLUMN)
        for besked in kontobeskeder:
            if besked in csv_data[CSV_MESSAGE_COLUMN].values:
                # Append the row to the dataframe
                rows = csv_data[csv_data[CSV_MESSAGE_COLUMN] == besked].copy()
                rows[JSON_ID_COLUMN] = entry.get(JSON_ID_COLUMN)

                # Must append each row individually
                # Alternatively, use pd.concat([target_df, rows], ignore_index=True)
                # However, this will create a new dataframe and not append to the existing one
                for _, row in rows.iterrows():
                    # TODO: This generates a future warning
                    target_df.loc[len(target_df)] = row

                # Remove the row from the CSV data
                csv_data.drop(rows.index, inplace=True)

def GetPaymentsByNotes(target_df:pd.DataFrame, csv_data: pd.DataFrame, json_data) -> None:
    """This function is used to get payments by notes in the CSV file.
    An example of a note could be 'st.tv:1.th:4.tv' using : as a separator.
    The notes must be set manually in the CSV file under the column 'Noter'

    Args:
        target_df (pd.DataFrame): The dataframe to store the payments
        csv_data (pd.DataFrame): The CSV data
        json_data (list): The JSON data containing Ids corresponding to the ones in the CSV file
    """

    if CSV_NOTES_COLUMN not in csv_data.columns:
        return

    unprocessed_data = GetUnprocessedPayments(csv_data)

    for entry in JsonEntryGenerator(json_data):
        id = entry.get(JSON_ID_COLUMN)

        for index, row in unprocessed_data.iterrows():
            note = row[CSV_NOTES_COLUMN]
            if not pd.notna(note):
                continue
            if id not in note:
                continue
            row[JSON_ID_COLUMN] = id
            target_df.loc[len(target_df)] = row

            # Subtract the id from the notes
            new_note = note.replace(id, '').strip()
            if len(set(new_note)) <= 1: # Remove the row if the note is empty
                csv_data.drop(index, inplace=True)
                #unprocessed_data.drop(index, inplace=True)
            else:
                csv_data.loc[index, CSV_NOTES_COLUMN] = new_note
                #unprocessed_data.loc[index, CSV_NOTES_COLUMN] = new_note

def JsonEntryGenerator(json_data) -> Iterable[dict]:
    data = copy.deepcopy(json_data)
    for entry in data:
        kontobeskeder = entry.get(JSON_MESSAGE_COLUMN).strip().split(';')
        entry[JSON_MESSAGE_COLUMN] = kontobeskeder
        yield entry

def GetUnprocessedPayments(csv_data: pd.DataFrame) -> pd.DataFrame:
    if CSV_SUBJECT_COLUMN in csv_data.columns:
        if CSV_SUBJECT_TEXT in csv_data[CSV_SUBJECT_COLUMN].values:
            unprocessed_data = csv_data[csv_data[CSV_SUBJECT_COLUMN] == CSV_SUBJECT_TEXT]
            return unprocessed_data
    return pd.DataFrame()