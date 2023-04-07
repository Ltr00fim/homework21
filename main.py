from abc import ABC, abstractmethod


class Storage(ABC):
    """ Шаг 1. Реализация абстрактного класса Storage """
    @abstractmethod
    def __init__(self, items, capacity):
        """
        Инициализация полей

        :param items: словарь {item (название товара): number (целое число)}
        :param capacity: целое число
        """
        self.items = items
        self._capacity = capacity

    @abstractmethod
    def add(self, item, capacity):
        """
        Увеличение количества запаса у товара

        :param item: строка (объект, чей запас нужно увеличить)
        :param capacity: целое число (количество)
        """
        pass

    @abstractmethod
    def remove(self, item, capacity):
        """
        Уменьшение количества запаса у товара
        :param item: строка (объект, чей запас нужно уменьшить)
        :param capacity: целое число (количество)
        """
        pass

    @abstractmethod
    def get_free_space(self):
        """
        :return: Вернуть количество свободных мест
        """
        pass

    @abstractmethod
    def get_items(self):
        """
        :return: Возвращает содержание склада в словаре {товар: количество}
        """
        pass

    @abstractmethod
    def get_unique_items_count(self):
        """
        :return: Возвращает количество уникальных товаров.
        """
        pass


class Store(Storage):
    """ Шаг 2. Реализация класса Store """
    def __init__(self, items, capacity=100):
        super().__init__(items, capacity)

    def add(self, item, capacity):
        if item in self.items:
            self.items[item] += capacity
        else:
            self.items[item] = capacity

    def remove(self, item, capacity):
        if item in self.items and self.items[item] >= capacity:
            self.items[item] -= capacity
            return True
        else:
            return False

    def get_free_space(self):
        free = 0
        for item in self.items:
            free += self.items[item]
        return self._capacity - free

    def get_items(self):
        return self.items

    def get_unique_items_count(self):
        return len(self.items)


class Shop(Storage):
    """ Шаг 3. Реализация класса Shop """
    def __init__(self, items, capacity=20):
        super().__init__(items, capacity)

    def add(self, item, capacity):
        if item in self.items:
            self.items[item] += capacity
        else:
            if self.get_unique_items_count() < 5:
                self.items[item] = capacity

    def remove(self, item, capacity):
        if item in self.items and self.items[item] >= capacity:
            self.items[item] -= capacity
            return True
        else:
            return False

    def get_free_space(self):
        free = 0
        for item in self.items:
            free += self.items[item]
        return self._capacity - free

    def get_items(self):
        return self.items

    def get_unique_items_count(self):
        return len(self.items)


class Request:
    """ Шаг 4. Реализация класса Request """
    def __init__(self, text):
        text = text.split()
        self._from = text[4]
        self._to = text[6]
        self._amount = int(text[1])
        self._product = text[2]

    @property
    def from_(self):
        return self._from

    @property
    def to(self):
        return self._to

    @property
    def amount(self):
        return self._amount

    @property
    def product(self):
        return self._product

    def __repr__(self):
        return f'from = "{self.from_}",\n' \
               f'to =  "{self.to}",\n' \
               f'amount = "{self.amount}",\n' \
               f'product = "{self.product}"'


def main():
    """ Шаг 4. Основная программа """
    store = Store(
        {"item1": 10,
         "item2": 20,
         "item3": 30}
    )
    shop = Shop(
        {"item1": 10,
         "item2": 20,
         "item3": 30}
    )

    print(f'Здравствуйте, мы рады видеть Вас в нашем магазине\nТовары в наличии: {shop.get_items()}\nТовары на складе: {store.get_items()}')
    print('Вы можете выполнить несколько команд: ')
    print('Команда чтобы сделать заказ из магазина в склад: "Доставить {кол-во товара} {товар} из магазина в склад"')
    print('Комнада чтобы вернуть заказ из склад в магазин: "Доставить {кол-во товара} {товар} из склада в магазин"')
    print('"Завершить" - exit')

    while True:
        request_user = input()
        if request_user.lower() == 'завершить':
            print('До свидания')
            break

        request = Request(request_user)
        if request.to == 'магазин':
            req = store.remove(request.product, request.amount)
            if req:
                shop.add(request.product, request.amount)
            else:
                print('Нет товара на складе')
        else:
            req = shop.remove(request.product, request.amount)
            if req:
                store.add(request.product, request.amount)
            else:
                print('Нет товара на складе')

        print(f'Склад: {store.get_items()}')
        print(f'Магазин: {shop.get_items()}')


if __name__ == '__main__':
    main()
