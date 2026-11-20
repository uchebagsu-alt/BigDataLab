BEGIN;

	SELECT 
		e.employee_id,
		COUNT(s.sales_id) AS sales_count
	FROM
		employees e
	LEFT JOIN sales s ON s.employee_id = e.employee_id
	GROUP BY e.employee_id
	HAVING COUNT(s.sales_id) > 1000
	ORDER BY e.employee_id;

	UPDATE products
	SET class = 'A'
	WHERE category_id IN (
		SELECT
			pr.category_id
		FROM 
			products pr
		JOIN sales s ON s.product_id = pr.product_id
		GROUP BY pr.category_id
		HAVING SUM(s.total_price) > 5000
	);

	UPDATE products
	SET modify_timestamp = NOW()
	WHERE modify_timestamp IS NULL;
	
COMMIT;