# родительский класс Product
class Product:
    def __init__(self, name: str, price: float | int):
        """
        Конструктор Products, чтобы задать начальные свойства

        :param name (str): название товара
        :param price (float):  цена за килограмм
        """
        self.name = name
        self.__price = price

    def set_price(self, new_price: float | int):
        """
        Сеттер для безопасного изменения приватной цены товара

        :param new_price (float | int): новая цена товара
        """
        if new_price > 0:
            old_price = self.__price
            self.__price = new_price
            print(f"Цена {self.name} изменена c {old_price} на {self.__price}")
        else:
            print("Ошибка безопасности: Цена должна быть положительной!")

    def get_price(self) -> float | int:
        """
        Геттер для безопасного чтения приватной цены товара

        :return self.__price (float | int): текущая цена товара
        """
        return self.__price

    def calculate_cost(self) -> float | int:
        """
        Базовый метод расчета стоимости товара

        :return float | int: итоговая стоимость штучного товара
        """
        return self.get_price()

    def get_display_info(self) -> str:
        """
        Формирует базовую информацию о товаре для чека

        :return str: строка с информацией о товаре
        """
        return f"Товар: {self.name} | Цена: {self.get_price()} руб."


# дочерний класс WeighableProduct(Product): Весовой товар
class WeighableProduct(Product):
    def __init__(self, name: str, price: float | int, weight: float | int):
        """
        Конструктор весового товара

        :param name (str): название товара
        :param price (float | int): цена за килограмм
        :param weight (float | int): вес партии в кг
        """
        super().__init__(name, price)
        self.weight = weight

    def calculate_cost(self) -> float | int:
        """
        Переопределенный расчет стоимости весового товара (цена * вес)

        :return float | int: стоимость весового товара
        """
        return self.get_price() * self.weight

    def get_display_info(self) -> str:
        """
        Формирует информацию о весовом товаре для чека

        :return str: строка с информацией о весовом товаре
        """
        return f"Весовой товар: {self.name} | Вес: {self.weight} кг | Итого: {self.calculate_cost()} руб."


# дочерний класс PackagedProduct(Product): Товар в упаковке
class PackagedProduct(Product):
    def __init__(self, name: str, price: float | int, quantity: int):
        """
        Конструктор товара в упаковке

        :param name (str): название товара
        :param price (float | int): цена за одну штуку
        :param quantity (int): количество штук в упаковке
        """
        super().__init__(name, price)
        self.quantity = quantity

    def calculate_cost(self) -> float | int:
        """
        Переопределенный расчет стоимости упаковки (цена * количество)

        :return float | int: стоимость всей упаковки
        """
        return self.get_price() * self.quantity

    def get_display_info(self) -> str:
        """
        Формирует информацию об упаковочном товаре для чека

        :return str: строка с информацией об упаковке
        """
        return f"Упаковка: {self.name} | Количество: {self.quantity} шт. | Итого: {self.calculate_cost()} руб."


# cимуляция работы кассы
# формирование чека

# создаем товары (объекты)
milk = Product("Молоко", 100)
apples = WeighableProduct("Яблоки", 50, 2.5)
eggs = PackagedProduct("Яйца", 12, 10)

# складываем их в один список-корзину
cart = [milk, apples, eggs]
total_sum = 0

# проверка работы сеттера
milk.set_price(-200)

# проверка полимофизма
print()
print("--- Чек EcoMarket ---")
for product in cart:
    print(product.get_display_info())
    total_sum += product.calculate_cost()
print("---------------------")
print(f"ИТОГО К ОПЛАТЕ: {total_sum} руб.")
