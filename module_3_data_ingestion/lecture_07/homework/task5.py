# импорт модуля json
import json


# Создание переменной api_response_json
api_response_json = """ 
{ 
    "store": "StoreHub", 
    "orders": [ 
        {"id": 1, "total": 50}, 
        {"id": 2, "total": 200}, 
        {"id": 3, "total": 150} 
        ]
 } 
"""

# Преобразование JSON в словарь Python
data_dict = json.loads(api_response_json)

# Получение списка заказов ("orders")
orders = data_dict["orders"]

# Формирование списка high_value_orders
high_value_orders = [
    order_dict for order_dict in orders if order_dict["total"] > 100
]

# Добавление этого списка обратно в словарь
data_dict["high_value_orders"] = high_value_orders

# Преобразование обновлённого словарь обратно в JSON-строку
result = json.dumps(data_dict, ensure_ascii=False)

# Вывод итоговой JSON-строки
print(result)
