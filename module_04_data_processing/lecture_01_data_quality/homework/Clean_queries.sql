WITH num_employees AS (
    SELECT
        ctid, 
        employee_id,
        hire_date,
        ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY hire_date) as num_row
    FROM 
        silver.silver_employees
)

DELETE FROM silver.silver_employees
WHERE ctid IN (
    SELECT 
        ctid
    FROM num_employees
    WHERE num_row > 1
);

DELETE FROM silver.silver_employees 
WHERE employee_id IS NULL;

DELETE FROM silver.silver_sales 
WHERE employee_id IS NULL;

DELETE FROM silver.silver_employees as e
WHERE NOT EXISTS (
	SELECT 
		1
	FROM 
		silver.silver_sales as s
	WHERE s.employee_id = e.employee_id
);

UPDATE silver.silver_sales as s
SET
	shop_id = e.shop_id,
	city_id = e.city_id
FROM
	silver.silver_employees as e
WHERE 
	s.employee_id = e.employee_id;