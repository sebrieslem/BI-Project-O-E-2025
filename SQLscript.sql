
-- 1. Create Retailer Dimension Table
CREATE TABLE retailer_dim (
    retailer_id INT PRIMARY KEY ,
    retailer_name VARCHAR(255)
);

-- 2. Create Date Dimension Table
CREATE TABLE date_dim (
    date_id INT PRIMARY KEY AUTO_INCREMENT,
    invoice_date DATE,
    year INT,
    month INT,
    day INT
);

-- 3. Create Region Dimension Table
CREATE TABLE region_dim (
    region_id INT PRIMARY KEY AUTO_INCREMENT,
    region_name VARCHAR(255),
    state VARCHAR(255),
    city VARCHAR(255)
);

-- 4. Create Product Dimension Table
CREATE TABLE product_dim (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(255)
);

-- 5. Create Sales Method Dimension Table
CREATE TABLE sales_method_dim (
    sales_method_id INT PRIMARY KEY AUTO_INCREMENT,
    sales_method_name VARCHAR(255)
);

-- 6. Create Sales Fact Table
CREATE TABLE sales_fact (
    sales_id INT PRIMARY KEY AUTO_INCREMENT,
    retailer_id INT,
    date_id INT,
	region_id INT,
    product_id INT,
    sales_method_id INT,
    price_per_unit FLOAT,
    units_sold INT,
    total_sales FLOAT,
    operating_profit FLOAT,
    FOREIGN KEY (retailer_id) REFERENCES retailer_dim(retailer_id),
    FOREIGN KEY (date_id) REFERENCES date_dim(date_id),
    FOREIGN KEY (region_id) REFERENCES region_dim(region_id),
    FOREIGN KEY (product_id) REFERENCES product_dim(product_id),
    FOREIGN KEY (sales_method_id) REFERENCES sales_method_dim(sales_method_id)
);


