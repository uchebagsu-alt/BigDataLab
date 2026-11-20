# Перечень сущностей и их первичных ключей (PK)
## Список
<small>Схема: сущность - первичный ключ</small>
- categories - category_id
- cities - city_id
- countries - country_id
- customers - customer_id
- employees - employee_id
- products - product_id
- sales - sales_id
- shops - shop_id

## Обоснование на примере customers и categories
**Customers - customer_id**
1) Уникальный числовой индентификатор
2) ни отчего не зависит, например, от *first_name* (имя) или от *address* (адрес)
3) такой ключ удобно использовать в качестве внешнего ключа в других таблицах (например, в *sales*)

<br></br>
**categories - category_id**  
<small>Примечание: ситуация с *categories* индентична с *customers*</small>

1) Уникальный числовой индентификатор
2) ни отчего не зависит, например, от *category_name* (название категории)
3) такой ключ удобно использовать в качестве внешнего ключа в других таблицах (например, в *products*)
