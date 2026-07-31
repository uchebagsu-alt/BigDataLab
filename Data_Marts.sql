CREATE SCHEMA IF NOT EXISTS mart;

-- mart_daily_anomaly
CREATE OR REPLACE VIEW mart.mart_daily_anomaly AS
WITH 
	daily_revenue AS (
		SELECT 
        	s.shop_sk,
        	d.full_date,
        	s.date_key,
        	COALESCE(SUM(s.total_price), 0) AS revenue
    	FROM gold.fact_sales s
    	JOIN gold.dim_date d ON d.date_key = s.date_key
    	GROUP BY s.shop_sk, d.full_date, s.date_key
	),
 	expected_calculate AS (
		SELECT
        	shop_sk,
        	full_date,
        	revenue,
        	AVG(revenue) OVER (
            	PARTITION BY shop_sk 
            	ORDER BY date_key 
            	ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING
        	) AS expected_revenue
    	FROM daily_revenue
	)
SELECT 
	shop_sk,
	full_date,
	revenue,
    expected_revenue,
	(revenue - expected_revenue) / NULLIF(expected_revenue, 0) AS uplift
FROM expected_calculate;

-- mart_shop_daily
CREATE OR REPLACE VIEW mart.mart_shop_daily AS
WITH 
	daily_shop_revenue AS (
    SELECT 
        shop_sk,
        date_key,
        SUM(total_price) AS daily_revenue
    FROM gold.fact_sales
    GROUP BY shop_sk, date_key
)
SELECT 
    sh.shop_sk, 
    sh.shop_id,
    sh.shop_address,
    sh.country_id,
    sh.country_name,
    sh.city_id,
    sh.city_name,
    sh.city_zipcode,
    COALESCE(AVG(dsr.daily_revenue), 0) AS avg_daily_revenue
FROM gold.dim_shop sh
LEFT JOIN daily_shop_revenue dsr ON sh.shop_sk = dsr.shop_sk
GROUP BY 
    sh.shop_sk, sh.shop_id, sh.shop_address, sh.country_id, 
    sh.country_name, sh.city_id, sh.city_name, sh.city_zipcode;


-- mart_customer_behavior
CREATE OR REPLACE VIEW mart.mart_customer_behavior AS
WITH person_info AS (
    SELECT 
        cu.customer_sk, 
        cu.customer_id,
        COALESCE(SUM(s.total_price), 0) AS revenue,
        MAX(d.full_date) AS last_purchase_date
    FROM gold.dim_customer cu
    LEFT JOIN gold.fact_sales s ON cu.customer_sk = s.customer_sk
    LEFT JOIN gold.dim_date d ON s.date_key = d.date_key
    GROUP BY cu.customer_sk, cu.customer_id
)
SELECT 
    customer_sk,
    customer_id,
    revenue,
    last_purchase_date,
    CASE 
        WHEN last_purchase_date >= CURRENT_DATE - INTERVAL '90 days' THEN 'Active'
        WHEN last_purchase_date IS NULL THEN 'Never Bought'
        ELSE 'Inactive'
    END AS activity_status,
    CASE 
        WHEN revenue >= 10000 THEN 'Rich'
        WHEN revenue >= 1000 THEN 'Regular'
        ELSE 'Poor'
    END AS revenue_segment
FROM person_info;

-- mart_employee_performance
CREATE OR REPLACE VIEW mart.mart_employee_performance AS
SELECT 
	e.employee_sk,
	e.employee_id,
    e.first_name,
    e.last_name,
	COALESCE(SUM(s.total_price), 0) AS revenue,
	COALESCE(SUM(s.quantity), 0) AS quantity_sales,
	COUNT(s.sale_id) AS count_sales,
	DENSE_RANK() OVER (ORDER BY COALESCE(SUM(s.total_price), 0) DESC) AS employee_rank
FROM gold.dim_employee e
LEFT JOIN gold.fact_sales s ON s.employee_sk = e.employee_sk
WHERE e.is_current = True
GROUP BY e.employee_sk, e.employee_id, e.first_name, e.last_name;

-- mart_product_seasonality
CREATE OR REPLACE VIEW mart.mart_product_seasonality AS 
WITH 
	category_monthly_sales AS (
    	SELECT
        	c.category_sk,
        	c.category_name,
        	d.year_num,
        	d.month_num,
        	d.month_name,
        	COALESCE(SUM(s.total_price), 0) AS revenue,
        	COALESCE(SUM(s.quantity), 0) AS total_quantity
    	FROM gold.fact_sales s
		JOIN gold.dim_category c ON c.category_sk = s.category_sk
		JOIN gold.dim_date d ON d.date_key = s.date_key
    	GROUP BY c.category_sk, c.category_name, d.year_num, d.month_num, d.month_name
	)
SELECT
	category_sk,
    category_name,
    year_num,
    month_num,
    month_name,
    revenue,
    total_quantity,
	RANK() OVER (PARTITION BY year_num, month_num ORDER BY revenue DESC) AS sales_rank
FROM category_monthly_sales;
