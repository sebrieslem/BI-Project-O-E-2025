ALTER TABLE sales_fact 
ADD CONSTRAINT fk_retailer_id FOREIGN KEY (retailer_id) REFERENCES retailer_dim(retailer_id);
