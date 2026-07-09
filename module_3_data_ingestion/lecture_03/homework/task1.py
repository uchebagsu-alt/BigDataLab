"""предобработка данных
Бизнес-контекст:
Во входных данных EcoMarket часть полей товара пришла в «сырых» форматах:
числовые значения в виде строк, регионы — с повторами, а некоторые структуры
нужно подготовить для дальнейшей обработки. Необходимо привести данные
к корректным типам и продемонстрировать работу с пустыми коллекциями
(как система определяет «пусто / не пусто»).

Шаги выполнения:
Шаг 1: Инициализировать входные переменные (сырые данные).
Шаг 2: Выполнить явное преобразование типов (приведение строк к float/int).
Шаг 3: Выполнить преобразование коллекций (конвертация в list, set и tuple).
Шаг 4: Создать пустые коллекции двумя способами, где это возможно.
Шаг 5: Проверить «пустоту» коллекций через функцию bool().
Шаг 6: Вывести значения и их типы данных в консоль.
"""

# step 1
raw_sku = "CARROT-001"
raw_regions = ("Minsk", "Warsaw", "Berlin", "Warsaw")
raw_weight_str = "2.5"
raw_stock_str = "150"

# step 2
weight_kg = float(raw_weight_str)
stock_quantity = int(raw_stock_str)

# step 3
sku_as_list = list(raw_sku)
regions_list = list(raw_regions)
unique_regions = set(raw_regions)
regions_tuple = tuple(unique_regions)

# step 4
empty_list_1 = []
empty_list_2 = list()

empty_dict_1 = {}
empty_dict_2 = dict()

empty_tuple_1 = ()
empty_tuple_2 = tuple()

empty_set = set()

# step 5
not_empty_list = [1]
not_empty_dict = {"gmail": "ee@gmail.com"}
not_empty_tuple = (1,)
not_empty_set = {1}

print(bool(empty_list_1))
print(bool(empty_dict_1))
print(bool(empty_tuple_1))
print(bool(empty_set))

print(bool(not_empty_list))
print(bool(not_empty_dict))
print(bool(not_empty_tuple))
print(bool(not_empty_set))

# step 6
print(weight_kg, type(weight_kg))
print(stock_quantity, type(stock_quantity))
print(sku_as_list, type(sku_as_list))
print(regions_list, type(regions_list))
print(unique_regions, type(unique_regions))
print(regions_tuple, type(regions_tuple))
print(bool(empty_list_1))
print(bool(empty_dict_1))
print(bool(empty_tuple_1))
print(bool(empty_set))
print(bool(not_empty_list))
print(bool(not_empty_dict))
print(bool(not_empty_tuple))
print(bool(not_empty_set))
