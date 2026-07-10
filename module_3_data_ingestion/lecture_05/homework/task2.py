# инициализация переменных
product = " фермерский ТВОРОГ "
price = 4.567
qty = 3
csv_row = "milk,bread,cheese"
review = "Это лучший ТВОРОГ в городе!"
file_path = r"C:\EcoMarket\data\2025\january\sales.csv"

# нормализация названия товара
clean_product = product.strip().lower().title()
print(clean_product)

# формирование чека для клиента
total = price * qty
receipt = f'Чек "EcoMarket"\nТовар:\t{clean_product}\nКол-во:\t{qty} \nИтого:\t{total:.2f} руб.'
print(receipt)

# подготовка строки из CSV
items = csv_row.split(",")
clean_csv = " | ".join(items)
print(clean_csv)

# проверка отзыва клиента
if "творог" in review.lower():
    print("Отзыв относится к категории: Dairy", end=" ")

# работа с путём к файлу
print(file_path)
# r"" используется перед строкой, чтобы не учитывать специальные символы, например, \n, \t
