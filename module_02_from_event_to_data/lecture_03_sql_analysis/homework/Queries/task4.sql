UPDATE products
SET price = price * 1.10
WHERE category_id = (
	SELECT
		category_id
	FROM 
		categories
	WHERE category_name = 'Fruits'
);

DELETE FROM employees e
WHERE NOT EXISTS (
	SELECT 
		1
	FROM 
		sales s
	WHERE s.employee_id = e.employee_id
);

BEGIN;

	INSERT INTO employees (employee_id, first_name, middle_initial, last_name, birth_date, gender, city_id, shop_id, hire_date)
	VALUES (327, 'Monke', 'D', 'Luffy', '2009-11-11', 'M', 1, 1, '2009-11-11');

	INSERT INTO sales (sales_id, employee_id, customer_id, product_id, quantity, discount, total_price, sales_timestamp, transaction_number)
	VALUES (2000001, 327, 1, 1, 1, 0.2, 2.30, NOW(), 'T0002000001');

COMMIT;