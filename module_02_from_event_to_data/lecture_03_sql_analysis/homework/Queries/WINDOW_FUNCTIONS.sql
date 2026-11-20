WITH 
	sales_and_employees AS (
		SELECT
			s.sales_id,
			s.employee_id,
			s.total_price,
			DATE_TRUNC('month', s.sales_timestamp) as monthly,
			e.shop_id
		FROM 
			sales s
		JOIN employees e ON s.employee_id = e.employee_id
	),

	shop_geography AS (
    	SELECT 
			sh.shop_id,
			co.country_name
    	FROM 
			shops sh
    	JOIN cities ci ON sh.city_id = ci.city_id
    	JOIN countries co ON ci.country_id = co.country_id
	)

SELECT 
	se.monthly AS sale_month,
	SUM(se.total_price)::NUMERIC(16,2) AS monthly_revenue,
	LAG(SUM(se.total_price), 1, 0) OVER (ORDER BY se.monthly ASC)::NUMERIC(16,2) AS previous_monthly_revenue,
	SUM(se.total_price) - (LAG(SUM(se.total_price), 1, 0) OVER (ORDER BY se.monthly ASC))::NUMERIC(16,2) AS revenue_diff_vs_previous
FROM 
	sales_and_employees se
JOIN shop_geography sg ON se.shop_id = sg.shop_id
WHERE sg.country_name = 'Germany'
GROUP BY se.monthly
ORDER BY se.monthly ASC
LIMIT 24;