"""морковка мытая
Бизнес-контекст:
Система подсвечивает товары как «Хит продаж» и принимает решения по отображению
в приложении и пополнению остатков на основе бизнес-правил. Дополнительно показатели
товара могут меняться: цена повышается, складской остаток пересчитывается после поставки.
Реализованы проверки через операторы сравнения, логические операторы и расширенные операторы присваивания.

Шаги выполнения:
Шаг 1: Инициализировать исходные переменные товара и данные для проверки скидки.
Шаг 2: Рассчитать статус 'is_hit' (хит продаж).
Шаг 3: Вывести базовый статус хита на экран.
Шаг 4: Добавить расширенные проверки (поставщик, отображение, пополнение, блокировка).
Шаг 5: Проверить приоритеты логических операторов and/or со скобками и без.
Шаг 6: Изменить значения через расширенное присваивание (+=, *=, //=) и пересчитать триггеры.
"""

# step 1
product_name = "Морковь мытая"
price = 2.5
stock_quantity = 150
is_local_farm = True
is_hit = False
supplier = None

has_coupon = True
has_card = False
total = 10

# step 2
is_hit = price < 3 and is_local_farm

# step 3
print(f"Является ли товар хитом? {is_hit}")

# step 4
has_supplier = supplier is not None
can_show_in_app = has_supplier and stock_quantity > 0
needs_restock = (stock_quantity <= 20) or is_hit
is_blocked = not (is_local_farm)

print(f"Поставщик указан? {has_supplier}")
print(f"Показывать в приложении? {can_show_in_app}")
print(f"Нужно пополнение? {needs_restock}")
print(f"Товар заблокирован для акции? {is_blocked}\n")

# step 5
discount_without_brackets = has_coupon or has_card and total > 50
discount_with_brackets = (has_coupon or has_card) and total > 50

print(f"Скидка без скобок: {discount_without_brackets}")
print(f"Скидка со скобками: {discount_with_brackets}\n")

# step 6
price += 1.0
stock_quantity *= 2

boxes = stock_quantity
boxes //= 10

print(f"Цена после изменения: {price}")
print(f"Остаток после изменения: {stock_quantity}")
print(f"Полных коробок по 10 кг: {boxes}\n")

is_hit_updated = price < 3 and is_local_farm
needs_restock_updated = (stock_quantity <= 20) or is_hit_updated

print(f"Является ли товар хитом (после изменений)? {is_hit_updated}")
print(f"Нужно пополнение (после изменений)? {needs_restock_updated}")
