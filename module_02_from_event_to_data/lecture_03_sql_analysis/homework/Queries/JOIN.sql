SELECT 
    s.sales_id,
	pr.product_name,
	sh.address AS shop_address
FROM 
	sales s
JOIN products pr ON pr.product_id = s.product_id
JOIN employees e ON s.employee_id = e.employee_id
JOIN shops sh ON e.shop_id = sh.shop_id
LIMIT 10;