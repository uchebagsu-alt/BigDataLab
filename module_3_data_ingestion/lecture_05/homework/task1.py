# инициализация и разделение строки лога
raw_log = "ORDER-2025-01-15|FRT-APPLE-PL|+111 (23) 456-78-90| мИНсК "
order_id, product_code, raw_phone, raw_city = raw_log.split("|")

# разбор кода товара (product_code)
category = product_code[0:3]
region = product_code[-2:]
position_first_hyphen = product_code.find("-")
print(f"Позиция первого дефиса в коде товара: {position_first_hyphen}")

if product_code.startswith("FRT"):
    print("Код товара начинается с 'FRT'")
else:
    print("Код товара не начинается с 'FRT'")

# очистка телефона от лишних символов
clean_phone = ""
for char in raw_phone:
    if char.isdigit():
        clean_phone += char

length_phone = len(clean_phone)
print(f"Длина номера телефона: {length_phone}")

# приведение названия города к нормальному виду
city = raw_city.strip().lower().title()


# формирование итогового отчета
report = f"Заказ: {order_id}\nКатегория: {category} | Регион: {region}\nТелефон: {clean_phone}\nГород: {city}"
print(report)
