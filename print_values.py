import json
import sys


def main(filename):
    try:
        with open(filename, "r") as file:
            for dict_ in json.load(file):
                print(dict_)  # выводим данные
    except FileNotFoundError:
        print("Файл не найден")


if __name__ == '__main__':
    if len(sys.argv) > 2:
        main(filename=sys.argv[1])
    else:
        print("Укажите название файла с записями")
