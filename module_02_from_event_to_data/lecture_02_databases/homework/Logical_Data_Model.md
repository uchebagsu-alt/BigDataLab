<style>
    h3 {
        border: 2px solid #8b8b8b;
        border-radius: 8px;
        padding: 10px 16px;
        margin-top: 24px;
        color: #A8C8E8;
        background: #1A2A3A;
    }
    
    div.entity {
        border: 2px solid #575757;
        border-radius: 8px;
        padding: 16px 20px;
        margin-top: 24px;
        color: #C8D8E8;
    }

    div.entity table {
        color: #C8D8E8;
    }
    
    div.entity table th {
        background: #1E3040;
        color: #A8C8E8;
        border: 1px solid #2A4A5A;
    }
    
    div.entity table td {
        background: #162230;
        border: 1px solid #2A4A5A;
    }
    
    small {
        color: #8899AA;
    }

    * {
        scroll-margin-top: 20vh;  
    }
</style>

# Текстовое описание логической модели данных

Данная логическая модель описывает структуру базы данных для управления продажами в сети магазинов. Модель включает 8 основных сущностей и позволяет:
1) Управлять информацией о клиентах, сотрудниках и товарах
2) Отслеживать продажи
3) Учитывать географическую структуру (страны, города)

## Перечень всех сущностей с их атрибутами

<div class='entity'>

Обозначения:
- PK (PRIMARY KEY)
- FK (FOREIGN KEY) --> {сущность на которую ссылается}
- null - отсутсвие особенностей

</div>

<div class='entity'>
Быстрая навигация по сущностям:

- [categories](#categories)
- [cities](#cities)
- [countries](#countries)
- [customers](#customers)
- [employees](#employees)
- [products](#products)
- [sales](#sales)
- [shops](#shops)


</div>

<div class='entity'>
<a id="categories"></a>

### Сущность categories
Краткое описание: данная сущность хранит информацию о названии категории товара магазина.  
Список Атрибутов:  
|Атрибут|Тип атрибута|Особенность|Описание|
|:---|:---:|:---:|:---|
|category_id|SERIAL|PK|Индекс категории|
|category_name|VARCHAR(64)|null|Название категории|

</div>
<div class='entity'>
<a id="cities"></a>

### Сущность cities
Краткое описание: данная сущность хранит информацию о городах, где расположены магазины.    
Список Атрибутов:
|Атрибут|Тип атрибута|Особенность|Описание|
|:---|:---:|:---:|:---|
|city_id|SERIAL|PK|Индекс города|
|city_name|VARCHAR(64)|null|Название города|
|zipcode|SMALLINT|null|Почтовый индекс города|
|country_id|INTEGER|FK --> countries|Индекс страны,где находится данный город|

</div>
<div class='entity'>
<a id="countries"></a>

### Сущность countries
Краткое описание: данная сущность хранит информацию о странах, где расположены города сети магазинов.    
Список Атрибутов:
|Атрибут|Тип атрибута|Особенность|Описание|
|:---|:---:|:---:|:---|
|country_id|SERIAL|PK|Индекс страны|
|country_name|VARCHAR(64)|null|Название страны|
|country_code|CHAR(2)|null|Код страны(например, France -> FR)|

</div>
<div class='entity'>
<a id="customers"></a>

### Сущность customers
Краткое описание: данная сущность хранит информацию о клиентах магазинов.    
Список Атрибутов:
|Атрибут|Тип атрибута|Особенность|Описание|
|:---|:---:|:---:|:---|
|customer_id|SERIAL|PK|Индекс клиента|
|first_name|VARCHAR(64)|null|Имя клиента|
|middle_initial|CHAR(1)|null|Инициал клиента|
|last_name|VARCHAR(64)|null|Фамилия клиента|
|city_id|INTEGER|FK --> cities|Индекс города|
|address|VARCHAR(64)|null|Адрес|

</div>
<div class='entity'>
<a id="employees"></a>

### Сущность employees
Краткое описание: данная сущность хранит информацию о сотрудниках магазинов.  
Список Атрибутов:
|Атрибут|Тип атрибута|Особенность|Описание|
|:---|:---:|:---:|:---|
|employee_id|SERIAL|PK|Индекс сотрудника|
|first_name|VARCHAR(64)|null|Имя сотрудника|
|middle_initial|CHAR(1)|null|Инициал сотрудника|
|last_name|VARCHAR(64)|null|Фамилия сотрудника|
|birth_date|DATE|null|Дата рождения сотрудника|
|gender|CHAR(1)|null|Гендер сотрудника|
|city_id|INTEGER|FK --> cities|Город в котором сотрудник|
|shop_id|INTEGER|FK --> shops|Магазин в котором сотрудник|
|hire_date|DATE|null|Дата найма сотрудника|

</div>
<div class='entity'>
<a id="products"></a>

### Сущность products 
Краткое описание: данная сущность хранит каталог товаров.  
Список Атрибутов:
|Атрибут|Тип атрибута|Особенность|Описание|
|:---|:---:|:---:|:---|
|product_id|SERIAL|PK|Индекс товара|
|product_name|VARCHAR(64)|null|Название товара|
|price|NUMERIC(10,2)|null|Цена товара|
|category_id|INTEGER|FK --> categories|Категория товара|
|class|CHAR(1)|null|Класс товара(A,B,C)|
|modify_timestamp|DATETIME|null|Метка времени изменения товара|
|resistant|VARCHAR(3)|null|Есть ли устойчивость|
|is_allergic|VARCHAR(3)|null|Есть ли аллергенны|
|vitality_days|INTEGER|null|Срок годности товара|

</div>
<div class='entity'>
<a id="sales"></a>

### Сущность sales
Краткое описание: данная сущность хранит информацию о продажах.  
Список Атрибутов:
|Атрибут|Тип атрибута|Особенность|Описание|
|:---|:---:|:---:|:---|
|sales_id|SERIAL|PK|Индекс продажи|
|employee_id|INTEGER|FK --> employees|Индекс сотрудника|
|customer_id|INTEGER|FK --> customers|Индексы клиентов|
|product_id|INTEGER|FK --> products|Индекс товара|
|quantity|SMALLINT|null|Количество товаров|
|discount|NUMERIC(5,2)|null|Скидка|
|total_price|NUMERIC(10,2)|null|Итоговая сумма|
|sales_timestamp|DATETIME|null|Дата и время продажи|
|transaction_number|CHAR(11)|null|Номер транзакции|

</div>
<div class='entity'>
<a id="shops"></a>

### Сущность shops
Краткое описание: данная сущность хранит информацию о магазинах.  
Список Атрибутов:
|Атрибут|Тип атрибута|Особенность|Описание|
|:---|:---:|:---:|:---|
|shop_id|SERIAL|PK|Индекс магазина|
|city_id|INTEGER|FK --> cities|Индекс города|
|address|VARCHAR(64)|null|Адрес|

</div>

## Связи и кратности
<div class='entity'>

|Сущность A|Направление|Сущность B|Кратность|Внешний ключ|
|:---|:---:|:---:|:---:|:---|
|cities|-->|countries|M:1|cities.country_id|
|customers|-->|cities|M:1|customers.city_id|
|employees|-->|cities|M:1|employees.city_id|
|employees|-->|shops|M:1|employees.shop_id|
|products|-->|categories|M:1|products.category_id|
|sales|-->|customers|M:1|sales.customer_id|
|sales|-->|employees|M:1|sales.employee_id|
|sales|-->|products|M:1|sales.product_id|
|shops|-->|cities|M:1|shops.city_id|

</div>

## Обоснование кратности

- **Сущность *cities* связана с сущностью *countries* как M:1.** Объяснение: Множество city_id (городов) могут ссылаться на одну и ту же country_id (страну).  

- **Сущность *customers* связана с сущностью *cities* как M:1.** Объяснение: Множество customer_id (клиентов) могут ссылаться на один и тот же city_id (город).  
- **Сущность *employees* связана с сущностью *cities* как M:1.** Объяснение: Множество employee_id (сотрудников) могут ссылаться на один и тот же city_id (город).
- **Сущность *employees* связана с сущностью *shops* как M:1.** Объяснение: Множество employee_id (сотрудников) могут ссылаться на один и тот же shop_id (магазин).
- **Сущность *products* связана с сущностью *categories* как M:1.** Объяснение: Множество product_id (товаров) могут ссылаться на одну и ту же category_id (категорию).
- **Сущность *sales* связана с сущностью *customers* как M:1.** Объяснение: Множество sales_id (продаж) могут ссылаться на один и тот же customer_id (клиента).
- **Сущность *sales* связана с сущностью *employees* как M:1.** Объяснение: Множество sales_id (продаж) могут ссылаться на один и тот же employee_id (сотрудника).
- **Сущность *sales* связана с сущностью *products* как M:1.** Объяснение: Множество sales_id (продаж) могут ссылаться на один и тот же product_id (товар).
- **Сущность *shops* связана с сущностью *cities* как M:1.** Объяснение: Множество shop_id (магазинов) могут ссылаться на один и тот же city_id (город).