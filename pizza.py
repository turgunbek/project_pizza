EMOJI_MARGHERITA = '\U0001F9C0'
EMOJI_PEPPERONI = '\U0001F355'
EMOJI_HAWAIIAN = '\U0001F34D'


class Pizza:
    """Базовый класс для создания пиццы.
    Содержит атрибуты об имени, эмоджи, ингридиентах и размере пиццы.
    Содержит метод dict() для получения списка ингридиентов.
    """
    def __init__(self, name, emoji, ingredients, size='L'):
        self.name = name
        self.emoji = emoji
        self.ingredients = ingredients
        self.size = size

    def dict(self) -> dict:
        return {self.name: ', '.join(self.ingredients)}


class Margherita(Pizza):
    """Класс наследуется от базового класса Pizza."""
    def __init__(self):
        super().__init__('Margherita', EMOJI_MARGHERITA,
                         ['tomato sauce', 'mozzarella', 'tomatoes'])


class Pepperoni(Pizza):
    """Класс наследуется от базового класса Pizza."""
    def __init__(self):
        super().__init__('Pepperoni', EMOJI_PEPPERONI,
                         ['tomato sauce', 'mozzarella', 'pepperoni'])


class Hawaiian(Pizza):
    """Класс наследуется от базового класса Pizza."""
    def __init__(self):
        super().__init__('Hawaiian', EMOJI_HAWAIIAN,
                         ['tomato sauce', 'mozzarella', 'chicken',
                          'pineapples'])
