# Описание внешних ключей (FK)
## Список сущностей и их внешние ключи
<small>Схема: сущность - внешний ключ(сущность, с которой связывает ключ)</small>

- **sales** - *employee_id* (employees), *customer_id* (customers), *product_id* (products)
- **products** - *category_id* (categories)
- **employees** - *city_id* (cities), *shop_id* (shops)
- **customers** - *city_id* (cities)
- **shops** - *city_id* (cities)
- **cities** - *country_id* (countries)

Сущности, которые без внешних ключей:
- **categories** - null
- **countries** - null
