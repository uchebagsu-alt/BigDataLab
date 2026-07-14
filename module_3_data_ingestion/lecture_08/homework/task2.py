# инициализация данных
branches = [
    {"city": "Minsk", "revenue": 15000},
    {"city": "Warsaw", "revenue": 32000},
    {"city": "London", "revenue": 12000},
]


# написание декоратора audit_logger
def audit_logger(func):
    """
    Декоратор, который логирует запуск функции.
    :param func: исходная функция, которую обварачиваем
    :return: функция-обертка wrapper
    """

    def wrapper(*args, **kwargs):
        """
        Обертывает и вызывает исходную функцию, сохраняя и возвращая результат

        :param *args: позиционные аргументы для исходной функции.
        :param **kwargs: именованные аргументы для исходной функции.
        :return result: результат оригинальной функции.
        """

        print("[AUDIT] Запуск анализа...")
        result = func(*args, **kwargs)
        print("[AUDIT] Анализ завершен.")
        return result

    return wrapper


# написание основной функции get_sorted_report с декоратором
@audit_logger
def get_sorted_report(data_list):
    """
    Сортирует список по ключу "revenue", по убыванию

    :param data_list: список словарей с данными филиалов.
    :return: новый отсортированный список.
    """
    return sorted(data_list, key=lambda x: x["revenue"], reverse=True)


# вызов функции get_sorted_report
sorted_branches = get_sorted_report(branches)

# вывод результатов в консоль
print("Топ филиалов:")
for index, branch in enumerate(sorted_branches):
    print(f"{index + 1}. {branch['city']}: {branch['revenue']}")
