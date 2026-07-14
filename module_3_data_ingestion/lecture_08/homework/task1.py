# инициализация данных
SMALL_BATCH_LIMIT = 500


# создание функции calculate_batch
def calculate_batch(weight, price, discount=0.0):
    """
    Функция предназначена для расчета стоимости партии товара.
    Она считает сумму и автоматически определяет, превышен ли глобальный лимит
    SMALL_BATCH_LIMIT.

    :param weight: вес (в килограммах, обязательный)
    :param price: цена за килограмм (обязательный)
    :param discount: скидка (опциональный, по умолчанию 0.0)
    :return: кортеж из итоговой суммы (float) и флага превышения лимита (bool)
    """
    is_limit_exceeded = False
    final_sum = 0

    # Расчет итоговой стоимости и проверка лимита
    final_sum = weight * price * (1 - discount)
    is_limit_exceeded = final_sum > SMALL_BATCH_LIMIT

    return final_sum, is_limit_exceeded


# вызов функции calculate_batch с распаковкой результатов
carrot_sum, carrot_is_exceeded = calculate_batch(100, 4)
apple_sum, apple_is_exceeded = calculate_batch(50, 20, 0.10)

# вывод результатов в консоль
print(
    f"Партия 1 (Морковь): Сумма {carrot_sum}. Превышение лимита: {carrot_is_exceeded}"
)
print(
    f"Партия 2 (Яблоки): Сумма {apple_sum}. Превышение лимита: {apple_is_exceeded}"
)
