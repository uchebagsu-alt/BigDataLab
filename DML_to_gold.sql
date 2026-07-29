-- Заполнение таблицы dim_customer
INSERT INTO gold.dim_customer(
    customer_id, first_name, middle_initial,
    last_name, country_id, country_name, country_code,
    city_id, city_name, city_zipcode, address
)
SELECT DISTINCT
    cu.customer_id,
    cu.first_name,
    cu.middle_initial,
    cu.last_name,
    ci.country_id,
    con.country_name,
    con.country_code,
    cu.city_id,
    ci.city_name,
    ci.city_zipcode,
    cu.address
FROM silver.silver_customers cu
JOIN silver.silver_cities ci ON cu.city_id = ci.city_id
JOIN silver.silver_countries con ON ci.country_id = con.country_id;

-- Заполнение таблицы dim_employee
INSERT INTO gold.dim_employee(
    employee_id, first_name, middle_initial,
    last_name, birth_date, gender, hire_date,
    country_id, country_name, country_code,
    city_id, city_name, city_zipcode, valid_from_dt, 
    valid_to_dt, is_current
)
SELECT DISTINCT
    e.employee_id, 
    e.first_name, 
    e.middle_initial,
    e.last_name,
    e.birth_date, 
    e.gender,
    e.hire_date,
    ci.country_id,
    con.country_name,
    con.country_code,
    e.city_id,
    ci.city_name,
    ci.city_zipcode,
    COALESCE(e.hire_date::timestamp, '2000-01-01 00:00:00'::timestamp) AS valid_from_dt,
    '9999-12-31 23:59:59'::timestamp AS valid_to_dt,
    TRUE AS is_current
FROM silver.silver_employees e
JOIN silver.silver_cities ci ON e.city_id = ci.city_id
JOIN silver.silver_countries con ON ci.country_id = con.country_id;

-- Заполнение таблицы dim_shop
INSERT INTO gold.dim_shop(
    shop_id, shop_address, country_id,
    country_name, country_code, city_id,
    city_name, city_zipcode
)
SELECT DISTINCT
    s.shop_id,
    s.address as shop_address,
    ci.country_id,
    con.country_name,
    con.country_code,
    s.city_id,
    ci.city_name,
    ci.city_zipcode
FROM silver.silver_shops s
JOIN silver.silver_cities ci ON s.city_id = ci.city_id
JOIN silver.silver_countries con ON ci.country_id = con.country_id;

-- Заполнение таблицы dim_product
INSERT INTO gold.dim_product(
    product_id, product_name, price, 
    class, modify_timestamp, resistant, 
    is_allergic, vitality_days
)
SELECT DISTINCT
    product_id, 
    product_name, 
    price, 
    class,
    modify_timestamp, 
    resistant, 
    is_allergic,
    vitality_days
FROM silver.silver_products;

-- Заполнение таблицы dim_category
INSERT INTO gold.dim_category(category_id, category_name)
SELECT DISTINCT
    category_id, 
    category_name
FROM silver.silver_categories;

-- Заполнение таблицы dim_date (Генерация дат)
INSERT INTO gold.dim_date (
    date_key, full_date, day_of_week, 
    week_num, month_num, month_name, 
    quarter_num, year_num
)
SELECT DISTINCT
    CAST(TO_CHAR(d, 'YYYYMMDD') AS INT) AS date_key, -- Ключ вида 20240815
    d::DATE AS full_date,
    EXTRACT(ISODOW FROM d)::SMALLINT AS day_of_week,
    EXTRACT(WEEK FROM d)::SMALLINT AS week_num,
    EXTRACT(MONTH FROM d)::SMALLINT AS month_num,
    TRIM(TO_CHAR(d, 'Month')) AS month_name,
    EXTRACT(QUARTER FROM d)::SMALLINT AS quarter_num,
    EXTRACT(YEAR FROM d)::SMALLINT AS year_num
FROM generate_series('2020-01-01'::DATE, '2040-12-31'::DATE, '1 day'::interval) AS d;


-- Заполнение таблицы dim_time (Генерация времени)
INSERT INTO gold.dim_time (
    time_key, full_time, hour, 
    minute, second, day_part
)
SELECT DISTINCT
    CAST(TO_CHAR(t, 'HH24MISS') AS INT) AS time_key, -- Ключ вида 143000 (14:30:00)
    t::TIME AS full_time,
    EXTRACT(HOUR FROM t)::SMALLINT AS hour,
    EXTRACT(MINUTE FROM t)::SMALLINT AS minute,
    EXTRACT(SECOND FROM t)::SMALLINT AS second,
    CASE
        WHEN EXTRACT(HOUR FROM t) >= 6 AND EXTRACT(HOUR FROM t) < 12 THEN 'Morning'
        WHEN EXTRACT(HOUR FROM t) >= 12 AND EXTRACT(HOUR FROM t) < 18 THEN 'Afternoon'
        WHEN EXTRACT(HOUR FROM t) >= 18 AND EXTRACT(HOUR FROM t) < 22 THEN 'Evening'
        ELSE 'Night'
    END AS day_part
FROM generate_series('2000-01-01 00:00:00'::TIMESTAMP, '2000-01-01 23:59:59'::TIMESTAMP, '1 second'::interval) AS t;

-- Заполнение таблицы fact_sales
-- инкрементальная загрузка
INSERT INTO gold.fact_sales(
    employee_sk, customer_sk, product_sk, category_sk, 
    shop_sk, quantity, discount, total_price, 
    sales_timestamp, transaction_number, date_key, time_key
)
SELECT DISTINCT
    e.employee_sk,
    cu.customer_sk,
    pr.product_sk,
    cat.category_sk,
    sh.shop_sk,

    src.quantity,
    src.discount,
    src.total_price,
    src.sales_timestamp,
    src.transaction_number,

    CAST(TO_CHAR(src.sales_timestamp, 'YYYYMMDD') AS INT) AS date_key,
    CAST(TO_CHAR(src.sales_timestamp, 'HH24MISS') AS INT) AS time_key

FROM silver.silver_sales src

-- Подключение с изменения для получения сурогатных ключей
JOIN gold.dim_category cat ON cat.category_id = src.category_id
JOIN gold.dim_customer cu ON cu.customer_id = src.customer_id
JOIN gold.dim_employee e ON e.employee_id = src.employee_id AND e.is_current = TRUE
JOIN gold.dim_product pr ON pr.product_id = src.product_id
JOIN gold.dim_shop sh ON sh.shop_id = src.shop_id

WHERE src.sales_timestamp > (
    SELECT COALESCE(MAX(sales_timestamp), '1900-01-01 00:00:00'::TIMESTAMP) 
    FROM gold.fact_sales
);
