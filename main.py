import pandas as pd

# Read the mapping file
mapping_df = pd.read_csv('mapping/in.csv')

# Read the column mapping file
column_mapping_df = pd.read_csv('mapping/out.csv')

# Iterate over each row in the mapping DataFrame
for _, row in mapping_df.iterrows():
    # Extract the necessary information from the mapping
    bank_name = row['name']
    input_filename = f"in/{row['filename']}"
    header_row = row['header']
    end_row = row['end']

    # Determine the engine based on the file extension
    if input_filename.endswith('.xlsx'):
        engine = 'openpyxl'
    elif input_filename.endswith('.xls'):
        engine = 'xlrd'
    else:
        raise ValueError("Unsupported file format")

    # Calculate the number of rows to read
    nrows = end_row - header_row

    # Read the Excel file using the dynamic header and end row
    df = pd.read_excel(input_filename, 
                       skiprows=header_row - 1,
                       nrows=nrows,
                       engine=engine,
                       dtype=str
    )

    # Define the function to extract the preceding part of a string
    def extract_preceeding(value, delimiter='\n'):
        return str(value).split(delimiter)[0]

    # Define the function to clean up values
    def cleanup_values(value, delimiter='\n'):
        new_val = str(value).replace(delimiter, '')
        new_val = str(new_val).replace('nan', '')
        return new_val

    # Define the function to wrangle amounts only
    def wrangle_amounts_only(col: pd.Series) -> pd.Series:
        text_col = col.str.replace("\n", '')
        num_col = text_col.str.replace(",", '').str.replace(".", '')
        num_col = pd.to_numeric(num_col, errors='coerce')
        return num_col if not num_col.isna().all() else text_col

    # Process the column names to remove anything after a newline character
    df.columns = [extract_preceeding(col) for col in df.columns]

    # Process each column's values
    for col in df.columns:
        drop = df[col].isna().all()
        if drop:
            df.drop(col, axis=1, inplace=True)
            continue
        df[col] = df[col].apply(lambda x: extract_preceeding(x) if isinstance(x, str) else x)
        df[col] = wrangle_amounts_only(df[col])

    # Fill NaN values with an empty string
    df = df.fillna('')

    # Save the extracted data to a CSV file in the "format" folder
    format_filename = f"format/{bank_name}.csv"
    df.to_csv(format_filename, index=False)

    # Apply column transformations based on the column mapping
    bank_column_mapping = column_mapping_df[column_mapping_df['bank_name'] == bank_name]
    rename_dict = dict(zip(bank_column_mapping['original_column'], bank_column_mapping['new_column']))
    df = df.rename(columns=rename_dict)

    # Add missing columns and reorder
    df['Payee'] = ''
    df['Category'] = ''
    df = df[['Date', 'Payee', 'Category', 'Memo', 'Outflow', 'Inflow']]

    # Save the final formatted data to a CSV file
    output_filename = f"out/{bank_name}.csv"
    df.to_csv(output_filename, index=False)
