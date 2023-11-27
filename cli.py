import click
from random import randint
from typing import Type
from pizza import Pizza, Margherita, Pepperoni, Hawaiian
from decorators import log


EMOJI_COOK_MAN = '\U0001F468\u200D\U0001F373'
EMOJI_CLOCK = '\U0001F551'
EMOJI_MOTOR_SCOOTER = '\U0001F6F5'


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.option('--delivery', default=False, is_flag=True)
@click.option('--size', type=click.Choice(['L', 'XL']), default='L')
@click.argument('pizza_type', type=click.STRING)
def order(size: str, pizza_type: str, delivery: bool) -> None:
    """Готовит пиццу и доставляет её (или оставляет для самовывоза)"""
    menu = {
        'margherita': Margherita(),
        'pepperoni': Pepperoni(),
        'hawaiian': Hawaiian(),
    }

    pizza = menu.get(pizza_type.lower())
    if not pizza:
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
    click.echo(f'- {margherita.name} {margherita.emoji} : '
               f'{margherita.dict()[margherita.name]}')
    click.echo(f'- {pepperoni.name} {pepperoni.emoji} : '
               f'{pepperoni.dict()[pepperoni.name]}')
    click.echo(f'- {hawaiian.name} {hawaiian.emoji} : '
               f'{hawaiian.dict()[hawaiian.name]}')


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
