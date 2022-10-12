import datetime
import json
import os
import time

TOPICS = {  # формат словаря: {адрес топика: названия параметра (для краткости в жсоне)}
    "/devices/wb-msw-v3_21/controls/Temperature": "Temperature",
    "/devices/wb-msw-v3_21/controls/Current Motion": "Motion",
    "/devices/wb-msw-v3_21/controls/Sound Level": "Sound Level",
    "/devices/wb-ms_11/controls/Illuminance": "Illuminace"
}
JSON_FILENAME = "values.json"
with open(JSON_FILENAME, "w") as file:
    json.dump([], file)  # пишем в жсон пустой массив


def main():
    for topic_name, value_name in TOPICS.items():
        os.system("touch " + value_name)  # создать по файлу для записи последних значений
        # подписка на топик с перенаправлением вывода в созданный файл
        os.system(f'mosquitto_sub -t "{topic_name}" -v > {value_name} &')
    while True:
        time.sleep(5)  # каждые пять секунд

        values = {
            "box_number": 26,
            "datetime": datetime.datetime.now().isoformat()
        }

        for topic_name, value_name in TOPICS.items():  # читаем последние строки из всех файлов и пишем словарь
            while True:
                try:  # обработка исключения на случай того, что файл занят записью
                    with open(value_name, "r") as file:
                        last_value = file.readlines()[-1]
                        values[value_name] = last_value
                    break
                except:
                    time.sleep(0.001)

        with open(JSON_FILENAME, "r") as file:  # пишем словарь в конец жсона
            all_values = json.load(file)
        with open(JSON_FILENAME, "w") as file:
            all_values.append(values)
            json.dump(all_values, file)


if __name__ == '__main__':
    main()
