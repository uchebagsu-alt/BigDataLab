# Инициализация списка prices
prices = [100, -50, 300, 40, 800]

# Очистка данных
prices.remove(-50)

# Изменение списка
prices.append(150)

# Сортировка списка
prices.sort()

# Создание нового списка через List Comprehension
tax_prices = [price * 1.2 for price in prices if price > 100.0]

# Вывод в консоль
print(f"Базовый прайс (очищенный): {prices}")
print(f"Цены с НДС (>100): {tax_prices}")
print(f"Общая выручка: {sum(tax_prices)}")
print(f"Минимум: {min(tax_prices)}")
print(f"Максимум: {max(tax_prices)}")
