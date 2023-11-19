import pytest
from cli import log, order, menu, Margherita, Pepperoni, Hawaiian
from cli import bake, deliver, pickup
from click.testing import CliRunner


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


def test_order_command():
    """Тестирование команды Click order с использованием CliRunner()
    для имитации ввода и захвата вывода.
    Для удобства внутри организованы подтесты Тест 1, Тест 2, Тест 3, Тест 4
    """
    runner = CliRunner()

    # Тест 1: Проверяем создание объекта Margherita
    result = runner.invoke(order, ['--size', 'L', 'margherita'])
    assert 'bake' in result.output
    assert 'Margherita' in result.output
    assert 'L' in result.output
    assert 'Доставили' not in result.output

    # Тест 2: Проверяем создание объекта Pepperoni с доставкой
    result = runner.invoke(order, ['--size', 'XL', '--delivery', 'pepperoni'])
    assert 'bake' in result.output
    assert 'Pepperoni' in result.output
    assert 'XL' in result.output
    assert 'Доставили' in result.output

    # Тест 3: Проверяем создание объекта Hawaiian с самовывозом
    result = runner.invoke(order, ['--size', 'L', 'hawaiian'])
    assert 'bake' in result.output
    assert 'Hawaiian' in result.output
    assert 'L' in result.output
    assert 'Доставили' not in result.output

    # Тест 4: Проверяем случай, когда пицца не найдена в меню
    result = runner.invoke(order, ['--size', 'L', '4 сыра'])
    assert 'Пицца с именем 4 сыра не найдена в меню.' in result.output


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

    res_marg = f'- {margherita.name} {margherita.emoji} : {margherita.dict()}'
    res_pepp = f'- {pepperoni.name} {pepperoni.emoji} : {pepperoni.dict()}'
    res_hawa = f'- {hawaiian.name} {hawaiian.emoji} : {hawaiian.dict()}'

    assert res_marg in result.output
    assert res_pepp in result.output
    assert res_hawa in result.output


def test_bake_output(capsys):
    """Тестирование функции bake().
    Проверяется с использованием мок-объекта
    """
    pizza_mock = type('PizzaMock', (), {'name': 'TestPizza', 'size': 'L'})
    bake(pizza_mock)
    captured = capsys.readouterr()
    assert 'Приготовили TestPizza размера L' in captured.out


def test_deliver_output(capsys):
    """Тестирование функции deliver().
    Проверяется с использованием фикстуры capsys
    """
    deliver()
    captured = capsys.readouterr()
    assert 'Доставили' in captured.out


def test_pickup_output(capsys):
    """Тестирование функции pickup().
    Проверяется с использованием фикстуры capsys
    """
    pickup()
    captured = capsys.readouterr()
    assert 'Самовывоз' in captured.out


if __name__ == '__main__':
    pytest.main()
