# %% Imports
import argparse
import pandas as pd
import numpy as np

# %% Constants

# %% Argument parsing
parser = argparse.ArgumentParser(description='BudgetMakerPandas')

parser.add_argument('-d', '--delimiter', type=str, default=';', help='Delimiter used in the CSV file')
parser.add_argument('-e', '--encoding', type=str, default='UTF-8-SIG', help='Encoding of the CSV file')
parser.add_argument('-dec', '--decimal', type=str, default=',', help='Decimal separator used in the CSV file')
parser.add_argument('-th', '--thousands', type=str, default='.', help='Thousands separator used in the CSV file')

parser.add_argument('-s', '--subject', type=str, default='Emne', help='Title of the subject column')
parser.add_argument('-ss', '--subsubject', type=str, default='Underemne', help='Title of the subsubject column')
parser.add_argument('-a', '--amount', type=str, default='Beløb', help='Title of the amount column')

parser.add_argument('-i', '--input', type=str, default='input.csv', help='Path to the input CSV file')
parser.add_argument('-o', '--output', type=str, default='output.csv', help='Path to the output CSV file')

args = parser.parse_args()

# %% Check if the input file exists
try:
    with open(args.input, 'r', encoding=args.encoding) as f:
        pass
except FileNotFoundError:
    print('Input file not found! Make sure {} exists.'.format(args.input))
    exit()

# %% Main code
# Read the CSV file into a DataFrame
df = pd.read_csv(args.input, delimiter=args.delimiter, encoding=args.encoding, decimal=args.decimal, thousands=args.thousands,
                       dtype={args.subject: str, args.subsubject: str, args.amount: float})

# Fill NaN values in args.subject with a placeholder (e.g., 'No Category')
df[args.subject] = df[args.subject].fillna('No Category')

# Fill NaN values in subsubject column with a placeholder (e.g., 'No Subcategory')
df[args.subsubject] = df[args.subsubject].fillna('No Subcategory')

# Group by subject, subsubject, and then sum the amount column
grouped_df = df.groupby([args.subject, args.subsubject])[args.amount].sum().reset_index()

# Replace the placeholder with NaN in the resulting DataFrame
grouped_df[args.subsubject] = grouped_df[args.subsubject].replace('No Subcategory', np.nan)

# Group by subject, then sum the amount column
summarized_df = grouped_df.groupby(args.subject)[args.amount].sum().reset_index()

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
    category_data = grouped_df[grouped_df[args.subject] == row['Category']]
    
    # Iterate through the rows of the category
    for _, sub_row in category_data.iterrows():
        if pd.notna(sub_row[args.subsubject]):
            subcategory_df = pd.DataFrame({'Category': [f" - {sub_row[args.subsubject]}"], 'Amount': [sub_row[args.amount]]})
            category_df = pd.concat([category_df, subcategory_df], ignore_index=True)
    
    result_dfs.append(category_df)

# Concatenate the list of DataFrames into the final result DataFrame
result_df = pd.concat(result_dfs, ignore_index=True)

# Round the 'Amount' column to two decimal places
result_df['Amount'] = result_df['Amount'].round(2)

# Write the result to a new CSV file
result_df.to_csv(args.output, index=False, encoding=args.encoding, float_format='%.2f',
                 decimal=args.decimal, sep=args.delimiter)

print('Done!')
# %%
