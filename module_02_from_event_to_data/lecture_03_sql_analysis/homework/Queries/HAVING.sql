SELECT 
	pr.product_name,
	SUM(s.total_price)::NUMERIC(16,9) AS total_revenue,
	AVG(s.total_price)::NUMERIC(16,12) AS avg_sale
FROM 
	sales s
JOIN products pr ON s.product_id = pr.product_id
GROUP BY pr.product_name
HAVING SUM(s.total_price) > 400000
ORDER BY total_revenue DESC
LIMIT 10;