import csv
import sys

import matplotlib.pyplot as plt


def main(filename):
    try:
        with open(filename, "r") as file:
            reader = csv.reader(file, 'excel')
            headers = []
            data = []
            for row in reader:
                if not headers:
                    headers = list(row)
                    index_need = headers.index("Motion")
                else:
                    data.append(list(row)[index_need])
        x = [i for i in range(len(data))]
        plt.plot(x, data)
        plt.show()


    except FileNotFoundError:
        print("Файл не найден")


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        main(filename=sys.argv[1])
    else:
        print("Укажите название файла с записями")
