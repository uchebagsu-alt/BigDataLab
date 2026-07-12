# Создание словаря product
product = {"id": 105, "name": "Organic Buckwheat", "price": 3.50, "stock": 100}

# Изменение значения ключа "price"
product["price"] = 4.20

# Добавление нового ключа "category"
product["category"] = "Grains"

# Получение ключа "discount" с помощью .get()
discount_rate = product.get("discount", 0)

# Вывод на экран
print(product)
print(discount_rate)
