"""
Модуль для создания схем-таблиц.

Данный модуль импортируется в etl_pipeline.py.
Здесь описываем наши таблицы в виде Python-классов (ORM модели sqlalchemy).
"""

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import declarative_base


# Создаем Базовую Модель
Base = declarative_base()


# Создание схем-таблиц


class BronzeCountry(Base):
    """
    Справочник стран.
    Хранит информацию о странах, к которым привязаны города.
    """

    __tablename__ = "bronze_countries"
    __table_args__ = {"schema": "bronze"}

    country_id = Column(Integer, primary_key=True)
    country_name = Column(String)
    country_code = Column(String)


class BronzeCity(Base):
    """
    Справочник городов.
    Связан с таблицей BronzeCountry через country_id.
    """

    __tablename__ = "bronze_cities"
    __table_args__ = {"schema": "bronze"}

    city_id = Column(Integer, primary_key=True)
    city_name = Column(String)
    zipcode = Column(String)
    country_id = Column(
        Integer, ForeignKey("bronze.bronze_countries.country_id")
    )


class BronzeCategory(Base):
    """
    Справочник категорий товаров.
    Хранит информацию о категориях товаров
    """

    __tablename__ = "bronze_categories"
    __table_args__ = {"schema": "bronze"}

    category_id = Column(Integer, primary_key=True)
    category_name = Column(String)


class BronzeProduct(Base):
    """
    Справочник товаров.
    Связан с таблицей BronzeCategory через category_id.
    Хранит характеристики продукта и его стоимость.
    """

    __tablename__ = "bronze_products"
    __table_args__ = {"schema": "bronze"}

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    price = Column(Numeric(precision=10, scale=2))
    category_id = Column(
        Integer, ForeignKey("bronze.bronze_categories.category_id")
    )
    product_class = Column("class", String)

    modify_timestamp = Column(String)
    resistant = Column(String)
    is_allergic = Column(String)
    vitality_days = Column(Integer)


class BronzeShop(Base):
    """
    Справочник магазинов.
    Связан с таблицей BronzeCity через city_id.
    """

    __tablename__ = "bronze_shops"
    __table_args__ = {"schema": "bronze"}

    shop_id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey("bronze.bronze_cities.city_id"))
    address = Column(String)


class BronzeEmployee(Base):
    """
    Справочник сотрудников.
    Связан с таблицей BronzeCity для определения места жительства
    и с таблицей BronzeShop для определения места работы.
    """

    __tablename__ = "bronze_employees"
    __table_args__ = {"schema": "bronze"}

    employee_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    middle_initial = Column(String)
    last_name = Column(String)
    birth_date = Column(String)
    gender = Column(String)
    city_id = Column(Integer, ForeignKey("bronze.bronze_cities.city_id"))
    shop_id = Column(Integer, ForeignKey("bronze.bronze_shops.shop_id"))
    hire_date = Column(String)


class BronzeCustomer(Base):
    """
    Справочник клиентов.
    Связан с таблицей BronzeCity для хранения адреса проживания.
    """

    __tablename__ = "bronze_customers"
    __table_args__ = {"schema": "bronze"}

    customer_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    middle_initial = Column(String)
    last_name = Column(String)
    city_id = Column(Integer, ForeignKey("bronze.bronze_cities.city_id"))
    address = Column(String)


class BronzeSale(Base):
    """
    Таблица фактов: Транзакции продаж.
    Таблица связывающая сотрудника (BronzeEmployee), клиента (BronzeCustomer)
    и проданный товар (BronzeProduct).
    История продаж.
    """

    __tablename__ = "bronze_sales"
    __table_args__ = {"schema": "bronze"}

    sales_id = Column(Integer, primary_key=True)
    employee_id = Column(
        Integer, ForeignKey("bronze.bronze_employees.employee_id")
    )
    customer_id = Column(
        Integer, ForeignKey("bronze.bronze_customers.customer_id")
    )
    product_id = Column(
        Integer, ForeignKey("bronze.bronze_products.product_id")
    )
    quantity = Column(Integer)
    discount = Column(Numeric(precision=5, scale=2))
    total_price = Column(Numeric(precision=10, scale=2))
    sales_timestamp = Column(String)
    transaction_number = Column(String)
