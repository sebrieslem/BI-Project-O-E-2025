SHOW CREATE TABLE sales_fact;
ALTER TABLE sales_fact DROP FOREIGN KEY sales_fact_ibfk_1;
ALTER TABLE retailer_dim DROP PRIMARY KEY;
ALTER TABLE retailer_dim MODIFY COLUMN retailer_id INT AUTO_INCREMENT PRIMARY KEY;
