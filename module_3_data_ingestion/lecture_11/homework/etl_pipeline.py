"""
ETL-пайплайн для загрузки сырых данных в слой Bronze хранилища данных.

Данный скрипт автоматизирует процесс извлечения (Extract) данных из CSV-файлов
и их загрузки (Load) в реляционную базу данных.

Перед загрузкой скрипт автоматически создает схему bronze и инициализирует
структуру таблиц на основе ORM-моделей из модуля base_tables.py.

Требования к расположению файлов:
    Папка с исходными данными (по умолчанию называется source) должна
    находиться строго в той же директории, что и данный скрипт.

    Пример структуры:
    etl_pipeline.py
    base_tables.py
    source:
     -  countries.csv
     -  cities.csv
     -  sales.csv
     -  ...

Конфигурация файлов (словарь files):
    В блоке запуска (if __name__ == "__main__") инициализируется словарь files.
    В него необходимо вписывать названия файлов, которые мы хотим загрузить:
    - Ключ словаря: точное название CSV-файла (например "sales.csv").
    - Значение (config):
        1) "table" (str): имя таблицы в базе данных (например "bronze_sales").
        2) "chunk" (int | None): Размер пакета строк для загрузки. Для небольших
          файлов  -  None, для тяжелых файлов рекомендуется указывать размер
          (например 5000), чтобы не перегружать память.
"""

import time
from pathlib import Path

import pandas as pd
from base_tables import Base
from pandas import DataFrame
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError


def read_csv_file(
    csv_filepath: str | Path,
    cols: list[str] | list[int] = None,
) -> DataFrame:
    """
    Читает CSV файл и возвращает DataFrame.

    :param csv_filepath (str): путь к csv файлу для чтения
    :param cols (list[str] | list[int])(optional): список с конкретными названиями
    колонок для выборки, по умолчанию None - все колонки включены
    :return df(DataFrame): содержимое csv файла
    """
    try:
        # EXTRACT (Извлечение)
        print("Загрузка таблицы...")
        df = pd.read_csv(
            csv_filepath,
            sep=";",
            header="infer",
            encoding="cp1251",
            usecols=cols,
        )
        print("Файл успешно прочитан")

        return df
    except FileNotFoundError:
        print("Файл не найден! Проверьте файловый путь")

    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")


def load_to_sql(
    df: DataFrame,
    engine: Engine,
    schema_table_name: str,
    chunk: int | None = None,
):
    """
    DataFrame загружает в базу данных

    :param df (DataFrame): исходный DataFrame
    :param schema_table_name (str): название таблицы в базе данных
    """
    try:
        # LOAD (Загрузка)
        print("Загрузка в базу данных...")
        df.to_sql(
            name=schema_table_name,
            con=engine,
            schema="bronze",
            if_exists="append",
            index=False,
            chunksize=chunk,
        )

        print("Данные успешно загружены в DWH!")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")


def connect_engine(db_path: str) -> Engine:
    """
    Создает движок и проверяет подключение к базе данных.

    :param db_path (str): путь к базе данных
    :return engine (Engine): движок.
    """
    try:
        # Настраиваем Engine (подключение к базе в памяти)
        print("Подключение к хранилищу данных...")
        engine = create_engine(db_path, echo=False)

        with engine.connect():
            print("Подключение к базе данных успешно инициализировано!")

        return engine

    except SQLAlchemyError as e:
        print(f"Ошибка при подключении к базе данных: {e}")
        raise SystemExit("Не удалось подключиться к базе. Выход.") from None


# ___Основная программа___

if __name__ == "__main__":
    # засекаем время выполнения(мне было любопытно, ничего более)
    start_time = time.time()
    # названия csv файлов
    files = {
        "countries.csv": {"table": "bronze_countries", "chunk": None},
        "cities.csv": {"table": "bronze_cities", "chunk": None},
        "categories.csv": {"table": "bronze_categories", "chunk": None},
        "products.csv": {"table": "bronze_products", "chunk": None},
        "shops.csv": {"table": "bronze_shops", "chunk": None},
        "employees.csv": {"table": "bronze_employees", "chunk": None},
        "customers.csv": {"table": "bronze_customers", "chunk": None},
        "sales.csv": {"table": "bronze_sales", "chunk": 5000},
    }
    # Ищем, где наш скрипт
    BASE_DIR = Path(__file__).resolve().parent
    # Указываем названия папки с csv файлами
    DATA_DIR = BASE_DIR / "source"

    # Создаем движок
    DB_URL = "postgresql://postgres:postgres@localhost:5440/python_task3210"
    engine: Engine = connect_engine(DB_URL)

    # Проверяем есть ли схема bronze в db
    try:
        with engine.begin() as conn:
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS bronze;"))
        print("Схема 'bronze' проверена/создана успешно.")

    except SQLAlchemyError as e:
        print("Ошибка при проверки/создании bronze схемы")
        print(f"Подробнее об ошибке: {e}")
        raise SystemExit(
            "Выход из-за ошибки подготовки базы данных."
        ) from None

    # Импортировал модуль base_tables, инициализируя схем-таблицы
    # Даем команду движку физически создать таблицы в базе из base_tables.py
    Base.metadata.create_all(engine)
    print("Таблицы создались в базе из base_tables.py")

    for filepath, config in files.items():
        full_filepath: Path = DATA_DIR / filepath

        table: str = config["table"]
        chunk: int | None = config["chunk"]

        print(f"\n--- Обработка {filepath} ---")
        # Читаем файл
        df: DataFrame = read_csv_file(full_filepath)

        # Загружаем в базу
        if df is not None:
            load_to_sql(df, engine, table, chunk)
    # устанавливаем время окончания
    end_time = time.time()
    # Подсчет и вывод времени выполнения скрипта
    execution_time = end_time - start_time
    print(f"***********Выполнен скрипт за {execution_time}***********")
