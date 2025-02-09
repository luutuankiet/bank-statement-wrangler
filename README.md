# Bank Statements Processing

Utility script to help wrangle some bank statements into format imported to [YNAB](https://www.ynab.com/).

## Project Structure

- **in/**: Contains the raw Excel files for each bank.
- **format/**: Stores intermediate CSV files after initial processing.
- **out/**: Contains the final formatted CSV files and mapping files.
- **main.py**: The main script that orchestrates the data processing.
- **mapping/in.csv**: Specifies the input files and row ranges for each bank.
- **mapping/out.csv**: Defines the column transformations for each bank.

## Installation

1. Clone the repository:
   ```bash
   cd bank-statements-processing
   pip install -r requirements.txt
   ```

## Usage
1. Place the raw Excel files in the raw/ directory. Ensure the filenames match those specified in mapping.csv.

2. Update mapping/in.csv with the correct header and end row numbers for each bank's file.

3. Update mapping/out.csv to define how columns should be renamed for each bank.

4. run the main script `python main.py`