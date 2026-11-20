SELECT 
    s.transaction_number,
	pr.product_name,
    s.total_price,
	s.customer_id,
	s.sales_timestamp
FROM 
    sales s
JOIN products pr ON s.product_id = pr.product_id
WHERE s.total_price > 1500 AND pr.class = 'A'
ORDER BY s.sales_id ASC
LIMIT 10;