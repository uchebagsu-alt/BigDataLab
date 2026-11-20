# Инициализация данных
rows_range = range(1, 6)
rows = list(rows_range)

# Изменение по индексу
rows[2] = "Ремонт"

# Проверка наличия значения
if 5 in rows:
    print("Ряд 5 доступен")

# Выполнение среза
priority_rows = rows[0:3]

# Вывод в консоль
print(f"Список рядов: {rows}")
print(f"Приоритетные ряды: {priority_rows}")
