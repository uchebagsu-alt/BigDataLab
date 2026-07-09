# Список списков
daily_logs = [
    [500, 0, 1200],  # Касса 1 (Нормальная)
    [
        300,
        -999,
        800,
    ],  # Касса 2 (Сломалась посередине, 800 не должно посчитаться)
    [1500, 200],  # Касса 3 (Нормальная)
]

total_revenue = 0

for i, log in enumerate(daily_logs):
    print(f"--- Обработка Кассы №{i} ---")
    for index, value in enumerate(log):
        if value == -999:
            print("Аварийная остановка кассы!")
            break
        if value == 0:
            print("Пропуск сбоя")
            continue
        if value > 0:
            total_revenue += value
            print(f"Добавлено: {value}")

print("=== ИТОГ ДНЯ ===")
print(f"Общая выручка магазина: {total_revenue}")
