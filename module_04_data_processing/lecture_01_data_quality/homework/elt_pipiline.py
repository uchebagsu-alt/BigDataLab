"""
ETL-скрипт для переноса данных из слоя Bronze в слой Silver.

Выполняет чтение сырых таблиц, очистку и форматирование дат,
а потом загружает обработанные данные в схему silver.
"""

import time

import pandas as pd
from pandas import DataFrame, Series
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError, ProgrammingError, SQLAlchemyError
from sqlalchemy.types import Numeric


def load_to_sql(
    df: DataFrame,
    engine: Engine,
    schema_table_name: str,
    chunk: int | None = None,
    dtype_map: any = None,
):
    """
    DataFrame загружает в базу данных

    :param df: исходный DataFrame для загрузки.
    :param engine: объект подключения SQLAlchemy (Engine).
    :param schema_table_name: название таблицы в БД.
    :param chunk: размер пакета для вставки записей. Если None, загружает всё сразу.
    """
    try:
        # LOAD (Загрузка)
        print("Загрузка в базу данных...")
        df.to_sql(
            name=schema_table_name,
            con=engine,
            schema="silver",
            if_exists="append",
            index=False,
            chunksize=chunk,
            dtype=dtype_map,
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
        print(f"Ошибка SQLAlchemyError: {e}")
        raise SystemExit("Не удалось подключиться к базе. Выход.") from None


def read_from_bronze(table_name: str, engine: Engine) -> DataFrame | None:
    """
    Читает таблицу из схемы bronze.

    :param table_name: Имя исходной таблицы.
    :param engine: Объект подключения SQLAlchemy (Engine).
    :return: DataFrame или None, если произошла ошибка чтения.
    """
    try:
        df = pd.read_sql(f"SELECT * FROM bronze.{table_name}", engine)
        return df
    except ProgrammingError as e:
        print(f"Ошибка: схема/таблица {table_name} не найдена в базе данных")
        print(f"Подробнее: {e}")
    except OperationalError as e:
        print(f"Ошибка подключения при чтении: {e}")
    except SQLAlchemyError as e:
        print(f"Ошибка SQLAlchemyError: {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")


def validate_and_fix_date(
    date_ser: Series, include_time: bool = False
) -> Series:
    """
    Валидирует и исправляет date/timestamp.

    :param date_ser: Колонка pandas (Series) с датами
    :param include_time: Если True, сохраняет время (HH:MM:SS), иначе отсекает
    """

    str_ser = date_ser.astype(str).str.strip()
    is_empty = date_ser.isna() | str_ser.isin(
        ["", "nan", "null", "Null", "None", "NaT"]
    )

    # Заменяем точки и слэши на тире по всей колонке
    clean_ser = str_ser.str.replace(".", "-", regex=False).str.replace(
        "/", "-", regex=False
    )

    # Разбор кривых форматов. Они становяться Nat (Not a Time)
    parsed_ser = pd.to_datetime(
        clean_ser, dayfirst=True, format="mixed", errors="coerce"
    )

    default_value = pd.Timestamp("1900-01-01 00:00:00")

    # Невозможные date/timestamp (NaT) -> 1900-01-01 (00:00:00)
    result = parsed_ser.fillna(default_value)
    # Отмечаем что пустые ячейки, для дальнейшего удаления через dropna
    result[is_empty] = pd.NaT

    if not include_time:
        return result.dt.date

    return result


def validate_and_fix_num(num_ser: Series, is_money: bool = False):
    """
    Очищает числовые колонки.

    :param is_money: Если True — округляет до 2 знаков для NUMERIC,
    если False — Int64 для ID и другого.
    """
    clean_ser = (
        num_ser.astype(str).str.strip().str.replace(",", ".", regex=False)
    )
    # все нечисловые символы станут NaN
    parsed_num = pd.to_numeric(clean_ser, errors="coerce")

    if is_money:
        return parsed_num.round(2)
    else:
        return parsed_num.astype("Int64")


if __name__ == "__main__":
    start_time = time.time()

    # Настроки
    DB_URL = "postgresql://postgres:postgres@localhost:5440/python_task3210"
    BRONZE_TABLES: list[str] = [
        "bronze_categories",
        "bronze_cities",
        "bronze_countries",
        "bronze_customers",
        "bronze_employees",
        "bronze_products",
        "bronze_sales",
        "bronze_shops",
    ]
    DATE_COLUMNS = ["hire_date", "birth_date"]
    TIMESTAMP_COLUMNS = ["sales_timestamp", "modify_timestamp"]
    ID_COLUMNS = [
        "category_id",
        "city_id",
        "country_id",
        "customer_id",
        "employee_id",
        "product_id",
        "sales_id",
        "shop_id",
        "quantity",
        "vitality_days",
    ]
    MONEY_COLUMNS = ["total_price", "price", "discount"]
    CHUNK_SIZE = {"silver_sales": 5000}
    DEFAULT_CHUNK = None

    engine: Engine = connect_engine(DB_URL)
    silver_dfs: dict[str, DataFrame] = {}

    # Чтение и очистка
    print("\n***** Чтение и очистка *****")
    for table in BRONZE_TABLES:
        df = read_from_bronze(table, engine)
        if df is None:
            continue

        for col in df.columns:
            if col in DATE_COLUMNS:
                df[col] = validate_and_fix_date(df[col])
            elif col in TIMESTAMP_COLUMNS:
                df[col] = validate_and_fix_date(df[col], include_time=True)
                if col == "sales_timestamp":
                    df = df.dropna(subset=[col])
            elif col in ID_COLUMNS:
                df[col] = validate_and_fix_num(df[col])
            elif col in MONEY_COLUMNS:
                df[col] = validate_and_fix_num(df[col], is_money=True)

        # Сохраняем в словарь с новым именем
        table = table.replace("bronze_", "silver_")
        silver_dfs[table] = df

    # Подготовка базы данных (схемы)
    print("\n***** Подготовка схемы *****")
    try:
        with engine.begin() as conn:
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS silver;"))
        print("Схема 'silver' проверена/создана успешно.")

    except SQLAlchemyError as e:
        print("Ошибка при проверки/создании silver схемы")
        print(f"Подробнее об ошибке: {e}")
        raise SystemExit(
            "Выход из-за ошибки подготовки базы данных."
        ) from None

    # LOAD (Загрузка в silver)
    for table, df in silver_dfs.items():
        chunk = CHUNK_SIZE.get(table, DEFAULT_CHUNK)
        dtype_map = {
            col: Numeric(10, 2) for col in df.columns if col in MONEY_COLUMNS
        }
        load_to_sql(
            df,
            engine=engine,
            schema_table_name=table,
            chunk=chunk,
            dtype_map=dtype_map,
        )

    # Завершение
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"***********Выполнен скрипт за {execution_time:.2f}***********")
