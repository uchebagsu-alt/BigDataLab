--test2
GRANT INSERT, UPDATE ON sales TO data_engineer_trainee;

SET ROLE data_engineer_trainee;

UPDATE sales 
SET total_price = 250.00 
WHERE sales_id = 1; -- right now, it's working
