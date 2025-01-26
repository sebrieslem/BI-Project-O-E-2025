SELECT `Retailer ID`, COUNT(DISTINCT `Retailer`) AS unique_retailers
FROM sales_data
GROUP BY `Retailer ID`
HAVING unique_retailers > 1;
