import datetime
import csv
import os
import time

TOPICS = {  # формат словаря: {адрес топика: названия параметра (для краткости в жсоне)}
    "/devices/wb-msw-v3_21/controls/Temperature": "Temperature",
    "/devices/wb-msw-v3_21/controls/Current Motion": "Motion",
    "/devices/wb-adc/controls/Vin": "Input Voltage"
}

CSV_FILENAME = "values.csv"
with open(CSV_FILENAME, "w") as file:
    writer = csv.DictWriter(file,
                            fieldnames=TOPICS.values()
                            )
    writer.writeheader()


def main():
    for topic_name, value_name in TOPICS.items():
        os.system("touch " + value_name)  # создать по файлу для записи последних значений
        # подписка на топик с перенаправлением вывода в созданный файл
        # os.system(f'mosquitto_sub -t "{topic_name}" > {value_name} &')

        os.system(
            'mosquitto_sub -t "' + topic_name + '" > "' + value_name + '" &')  # для версий, не поддерживающих f-строки

    while True:
        time.sleep(5)  # каждые пять секунд

        values = {
            "box_number": 26,
            "datetime": datetime.datetime.now().isoformat()
        }

        for topic_name, value_name in TOPICS.items():  # читаем последние строки из всех файлов и пишем словарь
            with open(value_name, "r") as file:
                last_value = file.readlines()[-1]
            last_value = float(last_value.replace("\n", ""))
            values[value_name] = last_value

        with open(CSV_FILENAME, "a") as file:
            writer = csv.DictWriter(file,
                                    fieldnames=TOPICS.values()
                                    )
            writer.writerow(values)


if __name__ == '__main__':
    main()
