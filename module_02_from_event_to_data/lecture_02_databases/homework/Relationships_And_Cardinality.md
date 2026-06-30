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
</style>

# Связи и кратности

<div class='entity'>

Типы связи:
- 1:1 (один к одному)
- 1:M (один ко многим) 
- M:1 (многие к одному)
- M:N (многие ко многим)


</div>
<div class='entity'>

## Связь между Sales и products
|Сущность A|Направление|Сущность B|Тип связи|  
|:---|:---:|:---:|:---:|
|sales|-->|products|M:1|
|products|-->|sales|1:M|

- **Сущность *sales* связана с сущностью *products* как M:1.** Объяснение: Множество sales_id (продаж) могут ссылаться на один и тот же product_id (товар).

</div>
<div class='entity'>

## Связь между employees и cities
|Сущность A|Направление|Сущность B|Тип связи|  
|:---|:---:|:---:|:---:|
|employees|-->|cities|M:1|
|cities|-->|employees|1:M| 

- **Сущность *employees* связана с сущностью *cities* как M:1.** Объяснение: Множество employee_id (сотрудников) могут ссылаться на один и тот же city_id (город).

</div>
<div class='entity'>

## Связь между cities и countries
|Сущность A|Направление|Сущность B|Тип связи|  
|:---|:---:|:---:|:---:|
|cities|-->|countries|M:1 |
|countries|-->|cities|1:M|

- **Сущность *cities* связана с сущностью *countries* как M:1.** Объяснение: Множество city_id (городов) могут ссылаться на одну и ту же country_id (страну). 

</div>