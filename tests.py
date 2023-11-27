import pytest
import re
from cli import log, order, menu, Margherita, Pepperoni, Hawaiian
from cli import bake, deliver, pickup
from click.testing import CliRunner


EMOJI_COOK_MAN = '\U0001F468\u200D\U0001F373'
EMOJI_CLOCK = '\U0001F551'
EMOJI_MOTOR_SCOOTER = '\U0001F6F5'


def test_log_decorator(capsys):
    """Тестирование функции log с использованием фикстуры capsys
    """
    # Создаем тестовую функцию, которую мы собираемся декорировать
    def test_function():
        return 42

    # Создаем обернутую функцию с декоратором log
    decorated_function = log(test_function)

    # Вызываем обернутую функцию
    result = decorated_function()

    # Получаем захваченный вывод
    captured = capsys.readouterr()

    # Проверяем, что вывод содержит ожидаемое имя функции
    assert "test_function" in captured.out

    # Проверяем, что результат обернутой функции
    # соответствует ожидаемому значению
    assert result == 42


@pytest.mark.parametrize("size, pizza_type, delivery, expected_output", [
    ('L', 'margherita', False, 'bake.*Margherita.*L.*'),
    ('XL', 'pepperoni', True, r'bake.*Pepperoni.*XL[\s\S]*Доставили.*'),
    ('L', 'hawaiian', False, r'bake.*Hawaiian.*L[\s\S]*Ожидаем.*'),
    ('L', '4 сыра', False, 'Пицца с именем 4 сыра не найдена в меню.'),
])
def test_order_command(size, pizza_type, delivery, expected_output):
    """Тестирование команды Click order с использованием CliRunner()
    для имитации ввода и захвата вывода.
    Для повторяющихся паттернов использован параметрический тест.
    Используются регулярные выражения для нахождения ключевых слов в выводе.
    """
    runner = CliRunner()
    command = ['--size', size, '--delivery'] if delivery else ['--size', size]
    command.extend([pizza_type])

    result = runner.invoke(order, command)

    assert result.exit_code == 0
    match = re.search(expected_output, result.output)
    assert match is not None, (f'Expected output not found.'
                               f'Actual output: {result.output}')


def test_menu_command():
    """Тестирование команды Click menu с использованием CliRunner()
    для имитации ввода и захвата вывода.
    Проверяется корректность создания подклассов.
    """
    runner = CliRunner()

    # Тест: Проверяем вывод меню
    result = runner.invoke(menu)
    margherita = Margherita()
    pepperoni = Pepperoni()
    hawaiian = Hawaiian()

    res_marg = (
        f'- {margherita.name} {margherita.emoji} : '
        f'{margherita.dict()[margherita.name]}')
    res_pepp = (
        f'- {pepperoni.name} {pepperoni.emoji} : '
        f'{pepperoni.dict()[pepperoni.name]}')
    res_hawa = (
        f'- {hawaiian.name} {hawaiian.emoji} : '
        f'{hawaiian.dict()[hawaiian.name]}')

    assert res_marg in result.output
    assert res_pepp in result.output
    assert res_hawa in result.output


def test_bake_output(capsys, mocker):
    """Тестирование функции bake().
    Проверяется с использованием мок-объекта.
    Запатчено поведение randint.
    """
    pizza_mock = type('PizzaMock', (), {'name': 'TestPizza', 'size': 'L'})
    mocker.patch('cli.randint', return_value=2)
    bake(pizza_mock)
    captured = capsys.readouterr()
    expected_out = (f'bake{EMOJI_COOK_MAN} Приготовили '
                    f'TestPizza размера L за 2с!\n')
    assert captured.out == expected_out


def test_deliver_output(capsys, mocker):
    """Тестирование функции deliver().
    Проверяется с использованием фикстуры capsys.
    Запатчено поведение randint.
    """
    mocker.patch('cli.randint', return_value=2)
    deliver()
    captured = capsys.readouterr()
    expected_out = f'deliver{EMOJI_MOTOR_SCOOTER} Доставили за 2с!\n'
    assert captured.out == expected_out


def test_pickup_output(capsys, mocker):
    """Тестирование функции pickup().
    Проверяется с использованием фикстуры capsys.
    Запатчено поведение randint.
    """
    mocker.patch('cli.randint', return_value=2)
    pickup()
    captured = capsys.readouterr()
    expected_out = f'pickup{EMOJI_CLOCK} Самовывоз пиццы. Ожидаем 2с!\n'
    assert captured.out == expected_out


if __name__ == '__main__':
    pytest.main()
