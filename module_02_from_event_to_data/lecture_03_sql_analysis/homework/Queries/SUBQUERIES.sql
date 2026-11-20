SELECT 
	e.first_name,
	e.last_name,
	sh.address AS shop_address,
	s.total_price::NUMERIC(12,6) AS max_amount
FROM
	sales s	
JOIN employees e ON s.employee_id = e.employee_id
JOIN shops sh ON e.shop_id = sh.shop_id
WHERE s.total_price = (
	SELECT 
		total_price
	FROM 
		sales 
	ORDER BY total_price DESC
	LIMIT 1
);