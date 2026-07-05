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

	shops_geography AS (
		SELECT
			sh.shop_id,
			sh.address,
			co.country_name
		FROM
			shops sh
		JOIN cities ci ON sh.city_id = ci.city_id
    	JOIN countries co ON ci.country_id = co.country_id
	)

-- main query
SELECT 
	geo.country_name, -- Название страны
	geo.shop_id, -- Уникальный идентификатор магазина
	geo.address, -- Адрес магазина
	sales_data.sales_count AS total_sales_count,  -- Количество продаж конкретного магазина
	sales_data.total_revenue AS total_sales_amount, -- Общая сумма выручки магазина
	SUM(sales_data.total_revenue) OVER (PARTITION BY geo.country_name) AS country_total_amount, -- Общий оборот всей страны
	(sales_data.total_revenue / SUM(sales_data.total_revenue) OVER (PARTITION BY geo.country_name)) AS country_sales_share, -- Доля магазина от оборота страны
	DENSE_RANK() OVER (PARTITION BY geo.country_name ORDER BY sales_data.total_revenue DESC) AS shop_rank,  -- Ранг магазина по выручке внутри страны
	SUM(sales_data.total_revenue) OVER (PARTITION BY geo.country_name ORDER BY sales_data.total_revenue DESC) AS country_running_total -- Накопительный оборот по стране (нарастающий итог)
FROM (
	SELECT
		sae.shop_id,
		COUNT(sae.sales_id) AS sales_count,
		SUM(sae.total_price) AS total_revenue
	FROM
		sales_and_employees sae
	GROUP BY sae.shop_id
	HAVING COUNT(sae.sales_id) >= 2
) sales_data
JOIN shops_geography geo ON  sales_data.shop_id = geo.shop_id
ORDER BY 
	geo.country_name,
	shop_rank ASC
LIMIT 22;