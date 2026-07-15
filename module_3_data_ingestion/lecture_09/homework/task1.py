def calculate_purchase(product_name: str, weight: int, price: float):
    """
    Рассчитывает стоимость партии товара и индекс.

    :param product_name: название товара
    :param weight: вес партии
    :param price: цена за килограмм
    """
    try:
        numeric_weight = float(weight)
        total_cost = numeric_weight * price
        technical_index = 100 / numeric_weight

        print(f"Товар: {product_name}, Итоговая стоимость: {total_cost}$")
    except TypeError as te:
        print(f"Тип ошибки: {type(te)}")
        print(f"Сообщение: {te}")
    except ValueError as ve:
        print(f"Тип ошибки: {type(ve)}")
        print(f"Сообщение: {ve}")
    except ZeroDivisionError as ze:
        print(f"Тип ошибки: {type(ze)}")
        print(f"Сообщение: {ze}")
    finally:
        print("--- Проверка партии завершена ---")


calculate_purchase("Томаты", 100, 2.5)
calculate_purchase("Огурцы", "пятьдесят", 1.8)
calculate_purchase("Перец", 0, 4)
calculate_purchase("Зелень", [10], 5)
