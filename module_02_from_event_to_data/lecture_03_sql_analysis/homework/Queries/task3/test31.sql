--test1
CREATE USER data_engineer_trainee WITH PASSWORD 'eng228';

GRANT SELECT ON sales TO data_engineer_trainee;

SET ROLE data_engineer_trainee;

SELECT * FROM sales LIMIT 5;

INSERT INTO sales (sales_id, product_id, employee_id, total_price) 
VALUES (11111, 1, 1, 1.00); -- it's not working