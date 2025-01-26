import pandas as pd

# Load the cleaned CSV file
csv_path = r'C:\ProjectBI\cleaned_data.csv'
cleaned_data = pd.read_csv(csv_path)

# Preview the data
print(cleaned_data.head())
import mysql.connector

from sqlalchemy import create_engine

try:
    print("Attempting connection with SQLAlchemy...")  # Debug message
    engine = create_engine('mysql+pymysql://root:eslemsebri03*@localhost/Adidas_Sales')
    connection = engine.connect()
    print("Connected to the database using SQLAlchemy!")
    connection.close()
except Exception as e:
    print("Error connecting with SQLAlchemy:", e)  # Prints error details

# Assuming 'cleaned_data' is the DataFrame holding your cleaned data
cleaned_data.to_sql('sales_data', con=engine, if_exists='replace', index=False)
print("Data uploaded successfully!")

sales_data = pd.read_sql('SELECT * FROM sales_data', con=engine)

# 2. Populate product_dim
product_dim = sales_data[['Product']].drop_duplicates()
product_dim.columns = ['product_name']
product_dim.to_sql('product_dim', con=engine, if_exists='append', index=False)
print("product_dim populated!")

# 3. Populate region_dim
region_dim = sales_data[['Region', 'State', 'City']].drop_duplicates()
region_dim.columns = ['region_name', 'state', 'city']
region_dim.to_sql('region_dim', con=engine, if_exists='append', index=False)
print("region_dim populated!")

# 5. Populate sales_method_dim
sales_method_dim = sales_data[['Sales Method']].drop_duplicates()
sales_method_dim.columns = ['sales_method_name']
sales_method_dim.to_sql('sales_method_dim', con=engine, if_exists='append', index=False)
print("sales_method_dim populated!")

# Extract unique dates and add year, month, day
date_dim = sales_data[['Invoice Date']].drop_duplicates()
date_dim['year'] = pd.to_datetime(date_dim['Invoice Date']).dt.year
date_dim['month'] = pd.to_datetime(date_dim['Invoice Date']).dt.month
date_dim['day'] = pd.to_datetime(date_dim['Invoice Date']).dt.day

# Rename the column to match the MySQL schema
date_dim = date_dim.rename(columns={'Invoice Date': 'invoice_date'})

# Insert into the date_dim table
date_dim.to_sql('date_dim', con=engine, if_exists='append', index=False)
print("date_dim populated!")

# Extract unique retailer names
retailer_dim = sales_data[['Retailer']].drop_duplicates()
retailer_dim.columns = ['retailer_name']  # Rename to match the retailer_dim schema

# Insert the unique retailer names into the retailer_dim table
retailer_dim.to_sql('retailer_dim', con=engine, if_exists='append', index=False)
print("retailer_dim table populated!")


# Define chunk size (number of rows to process at a time)
chunk_size = 1000

# Read sales_data in chunks
for chunk in pd.read_sql('SELECT * FROM sales_data', con=engine, chunksize=chunk_size):
    # Map retailer_id
    retailer_dim = pd.read_sql('SELECT * FROM retailer_dim', con=engine)
    chunk = chunk.merge(retailer_dim, how='left', left_on='Retailer', right_on='retailer_name')

    # Map date_id
    date_dim = pd.read_sql('SELECT * FROM date_dim', con=engine)
    chunk = chunk.merge(date_dim, how='left', left_on='Invoice Date', right_on='invoice_date')

    # Map region_id
    region_dim = pd.read_sql('SELECT * FROM region_dim', con=engine)
    chunk = chunk.merge(region_dim, how='left', left_on=['Region', 'State', 'City'], right_on=['region_name', 'state', 'city'])

    # Map product_id
    product_dim = pd.read_sql('SELECT * FROM product_dim', con=engine)
    chunk = chunk.merge(product_dim, how='left', left_on='Product', right_on='product_name')

    # Map sales_method_id
    sales_method_dim = pd.read_sql('SELECT * FROM sales_method_dim', con=engine)
    chunk = chunk.merge(sales_method_dim, how='left', left_on='Sales Method', right_on='sales_method_name')

    # Select and rename the required columns for sales_fact
    fact_table = chunk[['retailer_id', 'date_id', 'region_id', 'product_id', 'sales_method_id',
                        'Price per Unit', 'Units Sold', 'Total Sales', 'Operating Profit']]
    fact_table.columns = ['retailer_id', 'date_id', 'region_id', 'product_id', 'sales_method_id',
                          'price_per_unit', 'units_sold', 'total_sales', 'operating_profit']

    # Insert data into the fact table incrementally
    fact_table.to_sql('sales_fact', con=engine, if_exists='append', index=False)

    print(f"Processed and inserted {len(chunk)} rows into the sales_fact table.")
    
print("All data processed and inserted into sales_fact table!")
