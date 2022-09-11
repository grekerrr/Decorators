import json
import hashlib
from datetime import date, datetime


class CountryReader():
    def __init__(self, file_name: str):
        self.cursor = - 1
        with open(file_name, 'r', encoding='utf8') as file:
            self.countries = json.load(file)

    def __iter__(self):
        return self

    def __next__(self):
        self.cursor += 1
        if self.cursor == len(self.countries):
            raise StopIteration
        return self.countries[self.cursor]['name']['common']


def decorator_parameters(file_name):
    def decorator(old_function):
        def new_function(*args, **kwargs):
            with open(file_name, 'a+', encoding='utf8') as file:
                file.write(f'Функция: "{old_function.__name__}"\nЗапуск: {date.today()} {datetime.now().time()}\n'
                           f'Аргументы функции: {args}, {kwargs}\n')
                result = old_function(*args, **kwargs)
                file.write(f'Результат: {result}\n\n')
            return result

        return new_function

    return decorator


def decorator(old_function):
    def new_function(*args, **kwargs):
        with open('decorator.txt', 'a+', encoding='utf8') as file:
            file.write(f'Функция: "{old_function.__name__}"\nЗапуск: {date.today()} {datetime.now().time()}\n'
                       f'Аргументы функции: {args}, {kwargs}\n')
            result = old_function(*args, **kwargs)
            file.write(f'Результат: {result}\n\n')
        return result

    return new_function


if __name__ == '__main__':
    countries_reader = CountryReader('countries.json')
    with open('result.txt', 'a+', encoding='utf8') as file:
        counter = 0
        for country in countries_reader:
            counter += 1
            file.write(f'{country} - https://en.wikipedia.org/wiki/{country.replace(" ", "_")}\n')
        file.write(f'\nНайдено {counter} стран')


    @decorator
    def LineReader(file_name: str):

        with open(file_name, 'r', encoding='utf8') as my_file:
            while True:
                line = my_file.readline()
                if line:
                    yield hashlib.md5(line.encode('utf8')).hexdigest()
                else:
                    break


    @decorator_parameters('decorator_parameters.txt')
    def LineReader_1(file_name: str):

        with open(file_name, 'r', encoding='utf8') as my_file:
            while True:
                line = my_file.readline()
                if line:
                    yield hashlib.md5(line.encode('utf8')).digest()
                else:
                    break


    for item in LineReader('result.txt '):
        print(item)

    for item in LineReader_1('result.txt '):
        print(item)