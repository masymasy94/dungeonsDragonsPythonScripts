# def find_constructor_values():
#     with open("./URL_OggettiMagici.txt", "r") as file_oggetti:
#
#         lista_url = file_oggetti.readlines()
#         shuffle(lista_url)
#         url_oggetti = [x.strip() for x in lista_url]
#         for index, url in enumerate(url_oggetti):
#             if len(url) > 0 and index == 0:  # len(url_oggetti):
#                 print(url)
#                 print(str(index + 1) + "/" + str(len(url_oggetti)))
#                 r = requests.get(url)
#                 if r.status_code == 200:
#                     obj = BeautifulSoup(r.content, 'html.parser')
#                     h_list = [x.text for x in obj.find(id='tab-description').find_all_next(['h2'], class_='')]
#                     p_list = [x.text for x in obj.find(id='tab-description').find_all_next('p')]
#                     mappa = dict(zip(h_list, p_list))
#                     mappa['Nome'] = obj.find(class_='product_title entry-title').string
#                     print(mappa)
#
#                 else:
#                     print(r.status_code)
#                     quit()


import random
import time
from typing import Dict

import requests
from bs4 import BeautifulSoup


class yolo:
    def __init__(self, indice: int, nome: str, tipo_tag: str):
        self.indice = indice
        self.nome = nome
        self.tipo_tag = tipo_tag


def stampa_vigliacca(yolo_list) -> str:
    tipo: str = ""
    rarita: str = ""
    sintonia: str = ""
    effetto: str = ""
    proprieta_secondarie: str = ""

    for yolo_item in yolo_list:
        if yolo_item.nome == 'Tipo':
            while len(yolo_list) >= (yolo_item.indice + 1) and yolo_list[yolo_item.indice + 1].tipo_tag == "p":
                tipo += yolo_list[yolo_item.indice + 1].nome
                yolo_list.pop(yolo_item.indice + 1)

            if len(yolo_list) >= yolo_item.indice:
                yolo_list.pop(yolo_item.indice)

        elif yolo_item.nome == 'Rarità':
            while len(yolo_list) >= (yolo_item.indice + 1) and yolo_list[yolo_item.indice + 1].tipo_tag == "p":
                rarita += yolo_list[yolo_item.indice + 1].nome
                yolo_list.pop(yolo_item.indice + 1)

            if len(yolo_list) >= yolo_item.indice:
                yolo_list.pop(yolo_item.indice)

        elif yolo_item.nome == 'Sintonia':
            while len(yolo_list) >= (yolo_item.indice + 1) and yolo_list[yolo_item.indice + 1].tipo_tag == "p":
                sintonia += yolo_list[yolo_item.indice + 1].nome
                yolo_list.pop(yolo_item.indice + 1)

            if len(yolo_list) >= yolo_item.indice:
                yolo_list.pop(yolo_item.indice)

        elif yolo_item.nome == 'Effetto':
            while len(yolo_list) >= (yolo_item.indice + 1) and yolo_list[yolo_item.indice + 1].tipo_tag == "p":
                effetto += yolo_list[yolo_item.indice + 1].nome
                yolo_list.pop(yolo_item.indice + 1)

            if len(yolo_list) >= yolo_item.indice:
                yolo_list.pop(yolo_item.indice)

        else:
            proprieta_secondarie += yolo_item.nome + "\n"
            while len(yolo_list) >= (yolo_item.indice + 1) and yolo_list[yolo_item.indice + 1].tipo_tag == "p":
                proprieta_secondarie += yolo_list[yolo_item.indice + 1].nome + "\n"
                yolo_list.pop(yolo_item.indice + 1)

            if len(yolo_list) >= yolo_item.indice:
                yolo_list.pop(yolo_item.indice)

            return f"""
result.add(
        Enchantment(
            "{tipo}",
            "{rarita}",
            "{sintonia}",
            "{effetto}",
            "{proprieta_secondarie}"
        )
)

"""


def main():
    with open("./URL_OggettiMagici.txt", "r") as file_oggetti:
        url_oggetti = file_oggetti.readlines()
        url_oggetti = [x.strip() for x in url_oggetti]
        for index, url in enumerate(url_oggetti):
            if len(url) > 0 and index <= len(url_oggetti):
                print(url)
                r = requests.get(url)
                if r.status_code == 200:
                    obj = BeautifulSoup(r.content, 'html.parser')
                    hp_map = []
                    index: int = 0
                    for x in obj.find(id='tab-description').find_all_next(['h2', 'h3', 'p']):
                        hp_map.append(yolo(index, x.text, x.name))
                        index += 1

                    hp_map.append(yolo(len(hp_map), 'Nome', 'h2'))
                    hp_map.append(yolo(len(hp_map), obj.find(class_='product_title entry-title').string, 'p'))

                    with open("result_oggetti.txt", "a") as text_file:
                        print(stampa_vigliacca(hp_map), file=text_file)
                        text_file.close()
                    print(stampa_vigliacca(hp_map))
                    time.sleep(random.randint(1, 3))

                else:
                    print(r.status_code)
                    quit()


if __name__ == '__main__':
    main()

