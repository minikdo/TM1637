import sys, os
import tm1637
import requests
from time import sleep
from requests.exceptions import ConnectionError, HTTPError

disp = tm1637.TM1637(3, 2)

URL = 'http://panel.minik.pl/get_metar'


def get_temp(url):
    try:
        r = requests.get(url)
    except ConnectionError, HTTPError:
        return [' ', 'E', 'r', 'r']

    if r.status_code != 200:
       return [' ', ' ', ' ', '-']

    temp = r.json()['temp']

    temp_list = list(str(temp))

    new_list = []

    for x in temp_list:
        try:
            y = int(x)
        except ValueError:
            new_list.append(x)
        else:
            new_list.append(int(y))

    if len(new_list) < 4:
        free = 4 - len(new_list)
    for a in range(free):
        new_list.insert(0, ' ')

    return new_list

def main():
    while True:
        disp.set_values(get_temp(URL))
#       disp.set_values(['D', 'U', 'P', 'A'])
        sleep(300)
        disp.clear()
        sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        disp.cleanup()
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
