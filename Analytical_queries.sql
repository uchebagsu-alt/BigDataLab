-- Выручка по категориям
SELECT 
	cat.category_id,
	cat.category_name,
	COALESCE (SUM(s.total_price), 0) AS revenue
FROM gold.fact_sales s
JOIN gold.dim_category cat ON s.category_sk = cat.category_sk
GROUP BY cat.category_name, cat.category_id
ORDER BY cat.category_id;

-- Топ-10 клиентов
SELECT
	cu.customer_id,
	cu.first_name,
	cu.middle_initial,
	cu.last_name,
	COALESCE (SUM(s.total_price), 0) AS spent_money 
FROM gold.fact_sales s
JOIN gold.dim_customer cu ON s.customer_sk = cu.customer_sk
GROUP BY cu.customer_id, cu.first_name, cu.last_name, cu.middle_initial
ORDER BY SUM(total_price) DESC
LIMIT 10;

-- Анализ продаж по сотрудникам
SELECT 
    e.employee_id,
    e.first_name,
    e.middle_initial,
    e.last_name,
    COUNT(s.sale_id) AS count_sales,
    COALESCE(SUM(s.total_price), 0) AS revenue_from_sales, 
    COALESCE(SUM(s.quantity), 0) AS quantity_of_goods
FROM gold.dim_employee e 
LEFT JOIN gold.fact_sales s ON e.employee_sk = s.employee_sk 
WHERE e.is_current = TRUE
GROUP BY e.employee_id, e.first_name, e.last_name, e.middle_initial
ORDER BY e.employee_id;

-- ТОП 10 самых продаваемых товаров за Октябрь
SELECT 
	p.product_id,
	p.product_name,
	COALESCE(SUM(s.quantity), 0) AS quantity_of_products
FROM gold.fact_sales s
JOIN gold.dim_product p ON s.product_sk = p.product_sk
JOIN gold.dim_date d ON s.date_key = d.date_key
WHERE d.month_num = 10
GROUP BY p.product_id, p.product_name
ORDER BY SUM(s.quantity) DESC
LIMIT 10;