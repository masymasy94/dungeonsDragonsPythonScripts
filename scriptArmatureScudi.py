import random
import time
from random import randint, shuffle
from typing import Dict

import requests
from bs4 import BeautifulSoup


def main():
    with open("./URL_ArmatureScudi.txt", "r") as file_armature:

        url_armature = [x.strip() for x in file_armature.readlines()]
        shuffle(url_armature)
        for index, url in enumerate(url_armature):
            if len(url) > 0 and index <= len(url_armature):
                print(url)
                r = requests.get(url)
                if r.status_code == 200:
                    obj = BeautifulSoup(r.content, 'html.parser')
                    h2_list = [x.text for x in
                               obj.find(id='tab-description').find_all_next('h2', class_='') if x.text != 'Altro']
                    p_list = [x.text for x in obj.find(id='tab-description').find_all_next('p')]
                    mappa = dict(zip(h2_list, p_list))
                    mappa['Nome'] = obj.find(class_='product_title entry-title').string
                    with open('result_armature_scudi.txt', 'a', encoding='utf-8') as out:
                        out.write(stampa_vigliacca(mappa))
                    time.sleep(random.randint(1, 3))

                else:
                    print(r.status_code)
                    quit()


def find_constructor_values():
    with open("./URL_ArmatureScudi.txt", "r") as file_armature:
        s = set()  # {'Forza Richiesta', 'Classe Armatura', 'Peso', 'Svantaggio Furtività', 'Costo', 'Descrizione'}
        lista_url = file_armature.readlines()
        shuffle(lista_url)
        url_armature = [x.strip() for x in lista_url]
        for index, url in enumerate(url_armature):
            if len(url) > 0 and index <= len(url_armature):
                print(url)
                r = requests.get(url)
                if r.status_code == 200:
                    obj = BeautifulSoup(r.content, 'html.parser')
                    h2_list = [x.text for x in
                               obj.find(id='tab-description').find_all_next('h2', class_='') if x.text != 'Altro']
                    s.update(h2_list)
                else:
                    print(r.status_code)
                    quit()

        print(s)


def stampa_vigliacca(mappa: Dict[str, str]) -> str:
    return f"""
result.add(
        Enchantment(
            "{mappa.get('Nome')}",
            "{mappa.get('Forza Richiesta')}",
            "{mappa.get('Classe Armatura')}",
             {mappa.get('Peso')},
            "{mappa.get('Svantaggio Furtività')}",
            "{mappa.get('Costo')}",
            "{mappa.get('Descrizione')}"
        )
)

"""


if __name__ == '__main__':
    main()
