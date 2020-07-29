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
    nome: str = ""
    proprieta_secondarie: str = ""
    gen = (filtered_items for filtered_items in yolo_list if filtered_items.tipo_tag != 'p')

    for yolo_item in gen:
        if yolo_item.nome == 'Tipo':
            i = yolo_item.indice
            list = []
            k = 1
            while (i+k) < len(yolo_list) and (yolo_list[i + k].tipo_tag == 'p' or yolo_list[i + k].tipo_tag == 'thead' or yolo_list[i + k].tipo_tag == 'tbody'):
                list.append(yolo_list[i + k].nome)
                k += 1

            tipo = "\n".join(list)

        elif yolo_item.nome == 'Nome':
            i = yolo_item.indice
            list = []
            k = 1
            while (i+k) < len(yolo_list) and (yolo_list[i + k].tipo_tag == 'p' or yolo_list[i + k].tipo_tag == 'thead' or yolo_list[i + k].tipo_tag == 'tbody'):
                list.append(yolo_list[i + k].nome)
                k += 1

            nome = "\n".join(list)

        elif yolo_item.nome == 'Rarità':
            i = yolo_item.indice
            list = []
            k = 1
            while (i+k) < len(yolo_list)  and (yolo_list[i + k].tipo_tag == 'p' or yolo_list[i + k].tipo_tag == 'thead' or yolo_list[i + k].tipo_tag == 'tbody'):
                list.append(yolo_list[i + k].nome)
                k += 1

            rarita = "\n".join(list)

        elif yolo_item.nome == 'Sintonia':
            i = yolo_item.indice
            list = []
            k = 1
            while (i+k) < len(yolo_list) and (yolo_list[i + k].tipo_tag == 'p' or yolo_list[i + k].tipo_tag == 'thead' or yolo_list[i + k].tipo_tag == 'tbody'):
                list.append(yolo_list[i + k].nome)
                k += 1

            sintonia = "\n".join(list)

        elif yolo_item.nome == 'Effetto':
            i = yolo_item.indice
            list = []
            k = 1
            while (i+k) < len(yolo_list) and (yolo_list[i + k].tipo_tag == 'p' or yolo_list[i + k].tipo_tag == 'thead' or yolo_list[i + k].tipo_tag == 'tbody'):
                list.append(yolo_list[i + k].nome)
                k += 1

            effetto = "\n".join(list)
        else:
            if yolo_list[yolo_item.indice].tipo_tag != 'thead' and yolo_list[yolo_item.indice].tipo_tag != 'tbody':
                i = yolo_item.indice
                list = []
                k = 1
                while (i+k) < len(yolo_list):
                    list.append(yolo_list[i + k].nome)
                    k += 1

                proprieta_secondarie = "\n".join(list)
                break

    return f"""
result.add(
        Enchantment(
            "{nome}",
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
        random.shuffle(url_oggetti)
        url_oggetti = [x.strip() for x in url_oggetti]
        for index, url in enumerate(url_oggetti):
            # url = "https://www.dungeonsanddragonsitalia.it/compendio/oggetti-magici/pergamene/pergamena-magica/"
            if len(url) > 0 and index <= len(url_oggetti):
                print(url)
                r = requests.get(url)
                if r.status_code == 200:
                    obj = BeautifulSoup(r.content, 'html.parser')
                    hp_map = []
                    hp_map.append(yolo(len(hp_map), 'Nome', 'h2'))
                    hp_map.append(yolo(len(hp_map), obj.find(class_='product_title entry-title').string, 'p'))

                    for x in obj.find_all('section'):
                        x.decompose()

                    for x in obj.find_all(class_='products columns-4'):
                        x.decompose()

                    for x in obj.find(id='tab-description').find_all_next(['h2', 'h3', 'p', 'thead', 'tbody']):
                        hp_map.append(yolo(len(hp_map), x.text, x.name))

                    with open("result_oggetti.txt", "a", encoding='utf-8') as text_file:
                        print(stampa_vigliacca(hp_map), file=text_file)
                        text_file.close()
                    print(stampa_vigliacca(hp_map))
                    time.sleep(random.randint(1, 3))

                else:
                    print(r.status_code)
                    quit()


if __name__ == '__main__':
    main()
