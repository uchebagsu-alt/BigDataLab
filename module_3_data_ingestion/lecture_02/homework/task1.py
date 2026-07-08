"""
Входные данные:
category_a: "Vegetables" (Ошибочно присвоено фруктам)
category_b: "Fruits" (Ошибочно присвоено овощам)
price_per_unit_a: 150 (цена за ящик партии фруктов)
quantity_a: 40 (количество ящиков партии фруктов)
vat_rate: 0.2 (НДС 20%)
"""

# инициализация переменных с ошибочными значениями категорий и свойствами товара
category_a = "Vegetables"
category_b = "Fruits"
price_per_unit_a = 150
quantity_a = 40
vat_rate = 0.2

# обмен значений переменных category_a и category_b
category_a, category_b = category_b, category_a

# Рассчёт общей стоимости партии товара (total_value)
total_value = (price_per_unit_a * quantity_a) + (
    price_per_unit_a * quantity_a * vat_rate
)

# Вывод в консоль
print(f"Текущая категория A: {category_a}")
print(f"Общая стоимость партии с НДС: {total_value}")
