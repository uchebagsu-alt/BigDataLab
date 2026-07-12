# Создание списка suppliers_log
suppliers_log = [
    "FreshFarm Inc",
    "GreenFields Ltd",
    "AgroWorld Co",
    "FreshFarm Inc",
    "GreenFields Ltd",
]

# Преобразование его в множество unique_suppliers
unique_suppliers = set(suppliers_log)

# Добавление нового поставщика
unique_suppliers.add("GreenFields Ltd")

# Проверка наличия "FreshFarm Inc" в множестве и вывод результата
print("FreshFarm Inc" in unique_suppliers)

# Вывод итогового множества и количества уникальных поставщиков
print(unique_suppliers)
print(len(unique_suppliers))
