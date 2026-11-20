CREATE OR REPLACE FUNCTION AvgSalesPerEmployee (emp_id INTEGER)
RETURNS NUMERIC(12,4) AS $$
DECLARE
    avg_price NUMERIC(12,4);
BEGIN
	SELECT COALESCE(AVG(total_price), 0) INTO avg_price
	FROM sales
	WHERE employee_id = emp_id;

	RETURN avg_price;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE VIEW FullStatShops AS 
WITH 
	sales_and_employees AS (
		SELECT
			e.shop_id,
			s.sales_id,
			s.total_price
		FROM 
			sales s
		JOIN employees e ON s.employee_id = e.employee_id
	),

	shop_geography AS (
    	SELECT 
			sh.shop_id,
			sh.shop_address,
			co.country_name
    	FROM 
			shops sh
    	JOIN cities ci ON sh.city_id = ci.city_id
    	JOIN countries co ON ci.country_id = co.country_id
	)

SELECT 
	geo.shop_id,
	geo.shop_address,
	geo.country_name,
	COUNT(sae.sales_id) AS total_sales_count,
	COALESCE(SUM(sae.total_price), 0) AS total_sales_amount
FROM 
	shop_geography geo
LEFT JOIN sales_and_employees sae ON geo.shop_id = sae.shop_id
GROUP BY geo.shop_id, geo.shop_address, geo.country_name
ORDER BY geo.country_name;