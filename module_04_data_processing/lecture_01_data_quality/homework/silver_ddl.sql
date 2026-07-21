CREATE SCHEMA IF NOT EXISTS silver;

CREATE TABLE silver.silver_categories (
    category_id INT,
    category_name VARCHAR(64)
);

CREATE TABLE silver.silver_cities (
    city_id INT,
    city_name VARCHAR(64),
	zipcode VARCHAR(20),
    country_id INT
);

CREATE TABLE silver.silver_countries (
    country_id INT,
    country_name VARCHAR(64),
	country_code CHAR(2)
);

CREATE TABLE silver.silver_customers (
    customer_id INT,
    first_name VARCHAR(64),
	middle_initial CHAR(1),
    last_name VARCHAR(64),
    city_id INT,
    address VARCHAR(64)
);

CREATE TABLE silver.silver_employees (
    employee_id INT,
    first_name VARCHAR(64),
	middle_initial CHAR(1),
    last_name VARCHAR(64),
    birth_date DATE,   
	gender CHAR(1),
	city_id INT,
	shop_id INT,
    hire_date DATE 
);

CREATE TABLE silver.silver_products (
    product_id INT,
    product_name VARCHAR(64),
	price NUMERIC(10,2),
    category_id INT,
	class CHAR(1),
	modify_timestamp TIMESTAMP,
	resistant BOOLEAN,
	is_allergic BOOLEAN,
    vitality_days INT
);

CREATE TABLE silver.silver_sales (
    sales_id INT,
	employee_id INT,
	customer_id INT,
	product_id INT,
	quantity INT,
	discount NUMERIC(10,2),
	total_price NUMERIC(10,2),
    sales_timestamp TIMESTAMP,
	transaction_number CHAR(11),
	city_id INT,     
    shop_id INT
);

CREATE TABLE silver.silver_shops (
    shop_id INT,
	city_id INT,
    address VARCHAR(64)
);