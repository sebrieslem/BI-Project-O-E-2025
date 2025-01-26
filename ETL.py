import pandas as pd
# Load the Excel file
excel_file = 'Adidas US Sales Datasets.xlsx'
excel_data = pd.read_excel(excel_file)
# Display the first few rows of the Excel data
#print("Excel Data:")
#print(excel_data.head())
# Load the CSV file
csv_file = 'data_sales.csv'
csv_data = pd.read_csv(csv_file)
# Display the first few rows of the CSV data
#print("\nCSV Data:")
#print(csv_data.head())
# Check if the column 'Operating Margin' exists in the Excel data
if 'Operating Margin' in excel_data.columns:
    excel_data = excel_data.drop(columns=['Operating Margin'])
    print("'Operating Margin' column removed from Excel data.")
else:
    print("'Operating Margin' column not found in Excel data.")
# Display the updated Excel data
#print("\nUpdated Excel Data:")
#print(excel_data.head())
# Check if columns match between the two datasets
if list(excel_data.columns) == list(csv_data.columns):
    # Vertically merge the datasets
    merged_data = pd.concat([excel_data, csv_data], ignore_index=True)
    print("Datasets merged successfully (vertical merge).")
else:
    print("The column names or order do not match between the datasets.")
    print("Excel Data Columns:", excel_data.columns)
    print("CSV Data Columns:", csv_data.columns)
# Display the merged data
#print("\nMerged Data:")
#print(merged_data.head())
# Convert 'Invoice Date' to datetime in the Excel dataset
merged_data['Invoice Date'] = pd.to_datetime(merged_data['Invoice Date'], errors='coerce')
# Optionally, check for any issues with conversion (e.g., invalid date format)
#print("\nConverted 'Invoice Date' column in merged data:")
#print(merged_data[['Invoice Date']].head())
#print(merged_data[['Invoice Date']].tail())
# Check the data type of the 'Price per Unit' column
price_per_unit_type = merged_data['Price per Unit'].dtype
print(f"The data type of 'Price per Unit' is: {price_per_unit_type}")
# Remove the dollar sign and any commas (if present) and convert to numeric
merged_data['Price per Unit'] = merged_data['Price per Unit'].replace({'\$': '', ',': ''}, regex=True)
# Convert 'Price per Unit' to numeric (float)
merged_data['Price per Unit'] = pd.to_numeric(merged_data['Price per Unit'], errors='coerce')

# Display the first few rows to verify
#print("Updated 'Price per Unit' column:")
#print(merged_data[['Price per Unit']].head())
#print(merged_data[['Price per Unit']].tail())
# Convert 'Units Sold' to numeric (if not already) and handle errors
merged_data['Units Sold'] = pd.to_numeric(merged_data['Units Sold'], errors='coerce')

# Convert to integers (rounding if necessary)
merged_data['Units Sold'] = merged_data['Units Sold'].fillna(0).astype(int)

# Display the first few rows to verify
#print("Updated 'Units Sold' column:")
#print(merged_data[['Units Sold']].head())
#print(merged_data[['Units Sold']].tail())
# Recalculate 'Total Sales'
merged_data['Total Sales'] = merged_data['Price per Unit'] * merged_data['Units Sold']

# Display the first few rows to verify
#print("Updated 'Total Sales' column:")
#print(merged_data[['Total Sales']].head())
#print(merged_data[['Total Sales']].tail())

# Clean 'Operating Profit' column
merged_data['Operating Profit'] = merged_data['Operating Profit'].replace({'\$': '', ',': ''}, regex=True)

# Convert to numeric
merged_data['Operating Profit'] = pd.to_numeric(merged_data['Operating Profit'], errors='coerce')

# Display the first few rows to verify
#print("Updated 'Operating Profit' column:")
#print(merged_data[['Operating Profit']].head())
#print(merged_data[['Operating Profit']].tail())
# Divide the values of the first 9649 rows in the 'Operating Profit' column by 10
merged_data.loc[:9648, 'Operating Profit'] = merged_data.loc[:9648, 'Operating Profit'] / 10

# Display the first few rows to verify
#print("Updated 'Operating Profit' column (first 9649 rows divided by 10):")
#print(merged_data[['Operating Profit']].head())
# Check for duplicate rows and count how many duplicates exist
duplicates = merged_data.duplicated().sum()
#print(f"Number of duplicate rows: {duplicates}")

# Remove duplicate rows
merged_data = merged_data.drop_duplicates()

# Display the first few rows to verify
#print("\nData after removing duplicates:")
#print(merged_data.head())
# Remove rows with NaN values
merged_data = merged_data.dropna()

# Display the first few rows to verify
#print("\nData after removing rows with NaN values:")
#print(merged_data.head())
# Sort rows by 'Invoice Date' in increasing order
cleaned_data = merged_data.sort_values(by='Invoice Date', ascending=True)


# Drop the 'Retailer ID' column
if 'Retailer ID' in cleaned_data.columns:
    cleaned_data = cleaned_data.drop(columns=['Retailer ID'])
    print("'Retailer ID' column removed from the cleaned data.")
else:
    print("'Retailer ID' column not found in the cleaned data.")

# Display the first few rows to verify
print("\nCleaned data sorted by 'Invoice Date':")
print(cleaned_data.head())

#Save the cleaned dataset to a CSV file
merged_data.to_csv(r'C:\ProjectBI\cleaned_data.csv', index=False)
print("Cleaned data has been saved successfully to C:\\ProjectBI\\cleaned_data.csv")


