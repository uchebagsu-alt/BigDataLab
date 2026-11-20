def calculate_total_delivery_cost(
    product_name: str,
    weights: list[float] | tuple[float, ...],
    prices: list[float] | tuple[float, ...],
    discount: None | float = None,
    currency_rate: int | float = 1,
    *extra_costs: float,
) -> dict[str, float]:
    """
    Рассчитывает общую стоимость доставки партии товаров.

    :param product_name: Название товара
    :param weights: Веса упаковок
    :param prices: Цены за единицу веса
    :param discount: Процент скидки (например, 0.1 для 10%)
    :param currency_rate: Валютный курс
    :param *extra_costs: Дополнительные расходы на доставку
    :return dict[str, float]: Словарь с именем товара и итоговой стоимостью.
    """

    sum_without_discount: float = 0.0
    sum_with_discount: float = 0.0
    extra_sum: float = 0.0
    final_sum: float = 0.0

    if len(weights) == len(prices):
        for weight, price in zip(weights, prices):
            once_sum: float = weight * price
            sum_without_discount += once_sum

        if discount is not None:
            sum_with_discount = sum_without_discount * (1 - discount)
        else:
            sum_with_discount = float(sum_without_discount)

        if extra_costs:
            for cost in extra_costs:
                extra_sum += cost

        final_sum = (sum_with_discount + extra_sum) * currency_rate
    else:
        print("Не совпадение длины weights и prices")

    return {product_name: final_sum}


vegetables_result = calculate_total_delivery_cost(
    "Овощная партия",
    [100, 50],
    [4, 6],
    0.1,
    1,
    20,
    15,
)

fruits_result = calculate_total_delivery_cost(
    "Фруктовая партия",
    (30, 20, 10),
    (15, 12, 18),
    None,
    1.2,
    25,
)

for product, cost in fruits_result.items():
    print(f"Товар: {product}, итоговая стоимость: {cost}")

for product, cost in vegetables_result.items():
    print(f"Товар: {product}, итоговая стоимость: {cost}")
