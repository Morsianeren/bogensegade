# %%
import pandas as pd
import numpy as np

# %%

# Constants
DATA_PATH = 'raw.csv'
SUBJECT_TITLE = 'Emne'
SUBSUBJECT_TITLE = 'Underemne'
AMOUNT_TITLE = 'Beløb'

ALL_TITLES = [SUBJECT_TITLE, SUBSUBJECT_TITLE, AMOUNT_TITLE]

DELIMITER = ';'
ENCODING = 'UTF-8-SIG'
DECIMAL = ','

# %% Actual code
# Read the CSV file into a DataFrame
df = pd.read_csv(DATA_PATH, delimiter=DELIMITER, encoding=ENCODING, decimal=DECIMAL,
                       dtype={SUBJECT_TITLE: str, SUBSUBJECT_TITLE: str, AMOUNT_TITLE: float})

# Fill NaN values in SUBSUBJECT_TITLE with a placeholder (e.g., 'No Subcategory')
df[SUBSUBJECT_TITLE].fillna('No Subcategory', inplace=True)

# Group by SUBJECT_TITLE, SUBSUBJECT_TITLE, and then sum the AMOUNT_TITLE column
grouped_df = df.groupby([SUBJECT_TITLE, SUBSUBJECT_TITLE])[AMOUNT_TITLE].sum().reset_index()

# Replace the placeholder with NaN in the resulting DataFrame
grouped_df[SUBSUBJECT_TITLE].replace('No Subcategory', np.nan, inplace=True)

# Group by SUBJECT_TITLE, then sum the AMOUNT_TITLE column
summarized_df = grouped_df.groupby(SUBJECT_TITLE)[AMOUNT_TITLE].sum().reset_index()

# Rename columns for clarity
summarized_df.columns = ['Category', 'Summed Amount']

# Sort the DataFrame by 'Category'
summarized_df.sort_values(by='Category', inplace=True)

# Sort the DataFrame by 'Summed Amount' in descending order
summarized_df.sort_values(by='Summed Amount', ascending=True, inplace=True)

# Create a list to store DataFrames for each category and subcategory
result_dfs = []

# Iterate through the rows of the summarized DataFrame
for index, row in summarized_df.iterrows():
    category_df = pd.DataFrame({'Category': [row['Category']], 'Amount': [row['Summed Amount']]})
    
    # Filter the grouped DataFrame for the current category
    category_data = grouped_df[grouped_df[SUBJECT_TITLE] == row['Category']]
    
    # Iterate through the rows of the category
    for _, sub_row in category_data.iterrows():
        if pd.notna(sub_row[SUBSUBJECT_TITLE]):
            subcategory_df = pd.DataFrame({'Category': [f" - {sub_row[SUBSUBJECT_TITLE]}"], 'Amount': [sub_row[AMOUNT_TITLE]]})
            category_df = pd.concat([category_df, subcategory_df], ignore_index=True)
    
    result_dfs.append(category_df)

# Concatenate the list of DataFrames into the final result DataFrame
result_df = pd.concat(result_dfs, ignore_index=True)

# Round the 'Amount' column to two decimal places
result_df['Amount'] = result_df['Amount'].round(2)

# Write the result to a new CSV file
result_df.to_csv('output.csv', index=False, encoding=ENCODING, decimal=DECIMAL, sep=DELIMITER)
# %%
