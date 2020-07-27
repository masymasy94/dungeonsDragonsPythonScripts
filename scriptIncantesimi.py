import random
import time
from typing import Dict

import requests
from bs4 import BeautifulSoup


def main():
    with open("./URL_incantesimi.txt", "r") as file_incantesimi:
        url_incantesimi = file_incantesimi.readlines()
        random.shuffle(url_incantesimi)
        url_incantesimi = [x.strip() for x in url_incantesimi]
        for index, url in enumerate(url_incantesimi):
            if len(url) > 0 and index <= len(url_incantesimi):
                print(url)
                r = requests.get(url)
                if r.status_code == 200:
                    print(r.headers)
                    obj = BeautifulSoup(r.content, 'html.parser')
                    h2_list = [x.text for x in obj.find(id='tab-description').find_all_next('h2')]
                    p_list = [x.text for x in obj.find(id='tab-description').find_all_next('p')]
                    mappa = dict(zip(h2_list, p_list))
                    mappa['Nome Italiano'] = obj.find(class_='product_title entry-title').string

                    with open("result_incantesimi.txt", "a") as text_file:
                        print(stampa_vigliacca(mappa), file=text_file)
                        text_file.close()
                    print(stampa_vigliacca(mappa))
                    time.sleep(random.randint(1, 3))

                else:
                    print(r.status_code)
                    quit()


def stampa_vigliacca(mappa: Dict[str, str]) -> str:
    return f"""
result.add(
        Enchantment(
            "{mappa.get('Nome Italiano')}",
            "{mappa.get('Nome Inglese')}",
             {mappa.get('Livello')[:-1]},
            "{mappa.get('Scuola di Magia') + add_rituale(mappa.get('Rituale'))}",
            "{mappa.get('Tempo di Lancio')}",
            "{mappa.get('Gittata')}",
            "{mappa.get('Componenti')}",
            "{mappa.get('Durata')}",
            "{mappa.get('Effetto')}"
        )
)

"""


def add_rituale(stringa: str) -> str:
    return "%s" % ("" if stringa == "No" else " (rituale)")


if __name__ == '__main__':
    main()
