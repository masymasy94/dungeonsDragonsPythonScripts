import random
import time
from typing import Dict

import requests
from bs4 import BeautifulSoup


def main():
    with open("./URL_Armi.txt", "r") as file_armi:

        url_armi = [x.strip() for x in file_armi.readlines()]
        s = {'Proprietà', 'Tipo di Danno', 'Peso', 'Danno',
             'Costo'}  # proprietà h2 totali da considerare nel costruttore
        for index, url in enumerate(url_armi):
            if len(url) > 0 and index <= len(url_armi):
                print(url)
                r = requests.get(url)
                if r.status_code == 200:
                    # print(r.headers)
                    # print(r.content)
                    obj = BeautifulSoup(r.content, 'html.parser')
                    h2_list = [x.text for x in
                               obj.find(id='tab-description').find_all_next('h2', class_='') if x.text != 'Altro']
                    p_list = [x.text for x in obj.find(id='tab-description').find_all_next('p')]
                    mappa = dict(zip(h2_list, p_list))
                    mappa['Nome'] = obj.find(class_='product_title entry-title').string
                    print(stampa_vigliacca(mappa))
                    with open('result_armi.txt', 'a', encoding='utf-8') as out:
                        out.write(stampa_vigliacca(mappa))
                    time.sleep(1)

                else:
                    print(r.status_code)
                    quit()


def stampa_vigliacca(mappa: Dict[str, str]) -> str:
    return f"""
result.add(
        Enchantment(
            "{mappa.get('Nome')}",
            "{mappa.get('Proprietà')}",
            "{mappa.get('Tipo di Danno')}",
             {mappa.get('Peso')},
            "{mappa.get('Danno')}",
            "{mappa.get('Costo')}"
        )
)

"""


if __name__ == '__main__':
    main()
