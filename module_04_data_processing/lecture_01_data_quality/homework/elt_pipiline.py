# TODO: написать Docstring

import time

import pandas as pd
from pandas import DataFrame
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError, ProgrammingError, SQLAlchemyError


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
            schema="silver",
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
        print(f"Ошибка SQLAlchemyError: {e}")
        raise SystemExit("Не удалось подключиться к базе. Выход.") from None


def read_from_bronze(table_name: str, engine: Engine):
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


def validate_and_fix_date():
    # TODO: Написать функцию validate_and_fix_date, которая пытается разобрать
    # TODO: кривые форматы (слэши) и проверяет реальность даты.
    # TODO: Невозможные даты (например, 2023-99-99) заменять на Technical Default -> 1900-01-01.
    pass


# region Основная программа
if __name__ == "__main__":
    start_time = time.time()

    # Создаем движок
    DB_URL = "postgresql://postgres:postgres@localhost:5440/python_task3210"
    engine: Engine = connect_engine(DB_URL)

    # region Чтение bronze
    bronze_tables_name: list[str] = ["bronze_categories", "bronze_cities"]
    dfs = {str: DataFrame}  # Словарь с результатами чтения

    for bronze_table in bronze_tables_name:
        dfs[bronze_table] = read_from_bronze(bronze_table, engine)
    # endregion

    # TODO: чистка dfs с помощью validate_and_fix_date

    # region Проверяем есть ли схема silver в db
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
    # endregion

    # TODO: отправка в silver очищеные данные с помощью load_to_sql

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"***********Выполнен скрипт за {execution_time}***********")

# endregion
