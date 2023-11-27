import click


def log(func):
    """Декоратор для вывода имени функции."""
    def wrapper(*args, **kwargs):
        click.echo(f'{func.__name__}', nl=False)
        result = func(*args, **kwargs)
        return result
    return wrapper
