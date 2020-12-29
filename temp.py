#!/usr/bin/env python2.7
import os
import sys
import requests
from requests.exceptions import ConnectionError, HTTPError
from time import sleep

import tm1637

# Rpi: GPIO3, GPIO2
disp = tm1637.TM1637(3, 2)

URL = 'http://panel.minik.pl/get_metar'


def display(string):
    """ Returns a four element list to be displayed. """

    char_list = list(str(string))

    new_list = []

    # Check if the value is int or not
    for x in char_list:
        try:
            y = int(x)
        except ValueError:
            new_list.append(x)
        else:
            new_list.append(int(y))

    # Add leading spaces to keep 4 characters
    if len(new_list) < 4:
        free = 4 - len(new_list)
        for a in range(free):
            new_list.insert(0, ' ')

    return new_list


def get_metar(url):
    """ Gets json with METAR weather """

    output = {'temp': '-',
              'press': '0'}

    try:
        r = requests.get(url)
    except ConnectionError, HTTPError:
        output['temp'] = 'Err'
        print 'Connection error'
        return output

    if r.status_code != 200:
        output['press'] = r.status_code
    else:
        output = r.json()

    return output


def main():
    while True:
        metar = get_metar(URL)
        disp.clear()
        disp.set_values(display(int(metar['press'])))
	# print(type(metar['press']))
	# print(metar['press'])
        sleep(3)
        disp.set_values(display(metar['temp']))
        sleep(300)


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
