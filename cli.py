import click
from random import randint
from typing import Type


EMOJI_MARGHERITA = '\U0001F9C0'
EMOJI_PEPPERONI = '\U0001F355'
EMOJI_HAWAIIAN = '\U0001F34D'
EMOJI_COOK_MAN = '\U0001F468\u200D\U0001F373'
EMOJI_CLOCK = '\U0001F551'
EMOJI_MOTOR_SCOOTER = '\U0001F6F5'


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

    def dict(self) -> str:
        return ', '.join(self.ingredients)


class Margherita(Pizza):
    """Класс наследуется от базового класса Pizza.
    """
    def __init__(self):
        super().__init__('Margherita', EMOJI_MARGHERITA,
                         ['tomato sauce', 'mozzarella', 'tomatoes'])


class Pepperoni(Pizza):
    """Класс наследуется от базового класса Pizza.
    """
    def __init__(self):
        super().__init__('Pepperoni', EMOJI_PEPPERONI,
                         ['tomato sauce', 'mozzarella', 'pepperoni'])


class Hawaiian(Pizza):
    """Класс наследуется от базового класса Pizza.
    """
    def __init__(self):
        super().__init__('Hawaiian', EMOJI_HAWAIIAN,
                         ['tomato sauce', 'mozzarella', 'chicken', 'pineapples'])


def log(func):
    """Декоратор для вывода имени функции
    """
    def wrapper(*args, **kwargs):
        click.echo(f'{func.__name__}', nl=False)
        result = func(*args, **kwargs)
        return result
    return wrapper


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.option('--delivery', default=False, is_flag=True)
@click.option('--size', type=click.Choice(['L', 'XL']), default='L')
@click.argument('pizza_type', type=click.STRING)
def order(delivery: bool, size: str, pizza_type: str) -> None:
    """Готовит пиццу и доставляет её (или оставляет для самовывоза)"""
    pizza = None
    if pizza_type.lower() == 'margherita':
        pizza = Margherita()
    elif pizza_type.lower() == 'pepperoni':
        pizza = Pepperoni()
    elif pizza_type.lower() == 'hawaiian':
        pizza = Hawaiian()
    if pizza is None:
        click.echo(f'Пицца с именем {pizza_type} не найдена в меню.')
        return
    pizza.size = size

    bake(pizza)
    if delivery:
        deliver()
    else:
        pickup()


@cli.command()
def menu() -> None:
    """Выводит меню"""
    margherita = Margherita()
    pepperoni = Pepperoni()
    hawaiian = Hawaiian()
    click.echo(f'- {margherita.name} {margherita.emoji} : {margherita.dict()}')
    click.echo(f'- {pepperoni.name} {pepperoni.emoji} : {pepperoni.dict()}')
    click.echo(f'- {hawaiian.name} {hawaiian.emoji} : {hawaiian.dict()}')


@log
def bake(pizza: Type[Pizza]) -> None:
    """Готовит пиццу"""
    time_to_bake = randint(1, 5)
    click.echo(f'{EMOJI_COOK_MAN} Приготовили {pizza.name}'
               f' размера {pizza.size} за {time_to_bake}с!')


@log
def deliver() -> None:
    """Доставляет пиццу"""
    time_to_deliver = randint(1, 3)
    click.echo(f'{EMOJI_MOTOR_SCOOTER} Доставили за {time_to_deliver}с!')


@log
def pickup() -> None:
    """Ожидаем самовывоз пиццы"""
    time_to_wait = randint(1, 4)
    click.echo(f'{EMOJI_CLOCK} Самовывоз пиццы. Ожидаем {time_to_wait}с!')


if __name__ == '__main__':
    cli()
