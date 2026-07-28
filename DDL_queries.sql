-- Создание схемы gold
CREATE SCHEMA IF NOT EXISTS gold;

-- Таблица клиентов
CREATE TABLE gold.dim_customer (
    customer_sk BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id INT NOT NULL UNIQUE, -- Бизнес-ключ (BK)
    first_name VARCHAR NOT NULL,
    middle_initial CHAR(1),
    last_name VARCHAR NOT NULL,
    country_id INT NOT NULL,
    country_name VARCHAR NOT NULL,
    country_code CHAR(2) NOT NULL,
    city_id BIGINT NOT NULL,
    city_name VARCHAR NOT NULL,
    city_zipcode VARCHAR,
    address VARCHAR NOT NULL
);

-- Таблица товаров
CREATE TABLE gold.dim_product (
    product_sk BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_id INT NOT NULL UNIQUE, -- Бизнес-ключ (BK)
    product_name VARCHAR NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    class CHAR(1),
    modify_timestamp TIMESTAMP,
    resistant BOOL,
    is_allergic BOOL,
    vitality_days INT
);

-- Таблица категорий
CREATE TABLE gold.dim_category (
    category_sk BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    category_id INT NOT NULL UNIQUE, -- Бизнес-ключ (BK)
    category_name VARCHAR NOT NULL
);

-- Таблица сотрудников
CREATE TABLE gold.dim_employee (
    employee_sk BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employee_id INT NOT NULL UNIQUE,
    first_name VARCHAR NOT NULL,
    middle_initial CHAR(1),
    last_name VARCHAR NOT NULL,
    birth_date DATE,
    gender CHAR(1),
    hire_date DATE NOT NULL,
    country_id INT NOT NULL,
    country_name VARCHAR NOT NULL,
    country_code CHAR(2) NOT NULL,
    city_id BIGINT NOT NULL,
    city_name VARCHAR NOT NULL,
    city_zipcode VARCHAR,
    valid_from_dt TIMESTAMP NOT NULL,
    valid_to_dt TIMESTAMP NOT NULL,
    is_current BOOL NOT NULL
);

-- Таблица магазинов
CREATE TABLE gold.dim_shop (
    shop_sk BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    shop_id INT NOT NULL UNIQUE, -- Бизнес-ключ (BK)
    shop_address VARCHAR NOT NULL,
    country_id INT NOT NULL,
    country_name VARCHAR NOT NULL,
    country_code CHAR(2) NOT NULL,
    city_id INT NOT NULL,
    city_name VARCHAR NOT NULL,
    city_zipcode VARCHAR
);

-- Таблица-календарь (даты)
CREATE TABLE gold.dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE, -- Бизнес-ключ (BK)
    day_of_week SMALLINT NOT NULL,
    week_num SMALLINT NOT NULL,
    month_num SMALLINT NOT NULL,
    month_name VARCHAR NOT NULL,
    quarter_num SMALLINT NOT NULL,
    year_num SMALLINT NOT NULL
);

-- Таблица времени
CREATE TABLE gold.dim_time (
    time_key INT PRIMARY KEY,
    full_time TIME NOT NULL UNIQUE, -- Бизнес-ключ (BK)
    hour SMALLINT NOT NULL,
    minute SMALLINT NOT NULL,
    second SMALLINT NOT NULL,
    day_part VARCHAR NOT NULL
);

-- Таблица продаж
CREATE TABLE gold.fact_sales (
    sale_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,  
    employee_sk BIGINT NOT NULL,
    customer_sk BIGINT NOT NULL,
    product_sk BIGINT NOT NULL,
    category_sk BIGINT NOT NULL,
    shop_sk BIGINT NOT NULL,
    quantity INT NOT NULL,
    discount NUMERIC(10,2) NOT NULL,
    total_price NUMERIC(10,2) NOT NULL,
    sales_timestamp TIMESTAMP NOT NULL,
    transaction_number VARCHAR(100) NOT NULL, -- Бизнес-ключ (BK)
    date_key INT NOT NULL,
    time_key INT NOT NULL,
    
    -- Внешние ключи (Foreign Keys)
    CONSTRAINT fk_sales_employee FOREIGN KEY (employee_sk) REFERENCES gold.dim_employee(employee_sk),
    CONSTRAINT fk_sales_customer FOREIGN KEY (customer_sk) REFERENCES gold.dim_customer(customer_sk),
    CONSTRAINT fk_sales_product FOREIGN KEY (product_sk) REFERENCES gold.dim_product(product_sk),
    CONSTRAINT fk_sales_category FOREIGN KEY (category_sk) REFERENCES gold.dim_category(category_sk),
    CONSTRAINT fk_sales_shop FOREIGN KEY (shop_sk) REFERENCES gold.dim_shop(shop_sk),
    CONSTRAINT fk_sales_date FOREIGN KEY (date_key) REFERENCES gold.dim_date(date_key),
    CONSTRAINT fk_sales_time FOREIGN KEY (time_key) REFERENCES gold.dim_time(time_key)
);