import random
import time
from typing import Dict

import requests
from bs4 import BeautifulSoup


def main():
    print('yolo')
    with open("./URL_Mostri.txt", "r") as file_mostri:
        url_mostri = [x.strip() for x in file_mostri.readlines()]
        for index, url in enumerate(url_mostri):
            if len(url) > 0 and index == 0:
                print(url)
                r = requests.get(url)
                if r.status_code == 200:
                    print(r.headers)
                    obj = BeautifulSoup(r.content, 'html.parser')
                    print(obj.find(id='tab-description'))
                else:
                    print(r.status_code)
                    quit()


if __name__ == '__main__':
    main()
