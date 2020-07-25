import itertools
import re
import time
from itertools import takewhile
from random import randint, shuffle
from typing import Dict, List, Tuple, Match, Any, Iterator, Optional, FrozenSet

import requests
from bs4 import BeautifulSoup, PageElement

__LIST_FIELDS: FrozenSet[str] = frozenset({
    'azioni',
    'azioni leggendarie',
    'reazioni'
})

__NAME_MAPPING: Dict[str, str] = {
    'sfida': 'challange',
    'classe armatura': 'armorClass',
    'punti ferita': 'hitPoints',
    'azioni': 'actions',
    'azioni leggendarie': 'legendaryActions',
    'nome': 'name',
    'taglia': 'size',
    'tipo': 'species',
    'allineamento': 'alignment',
    'velocità': 'speed',
    'tiri salvezza': 'savingThrows',
    'abilità': 'abilities',
    'sensi': 'senses',
    'linguaggi': 'languages',
    'resistenze al danno': 'resistenzaDanni',
    'immunità al danno': 'immunitaDanni',
    'resistenza alle condizioni': 'resistenzaCondizioni',
    'immunità alle condizioni': 'immunitaCondizioni',
    'forza': 'strenght',
    'destrezza': 'dexterity',
    'intelligenza': 'intelligence',
    'costituzione': 'constitution',
    'saggezza': 'wisdom',
    'carisma': 'charisma',
    'reazioni': 'reactions'
}


def get_content(r: requests.Response) -> Tuple[int, List[PageElement], Optional[str]]:
    if r.status_code == 200:
        # print(r.headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        content: List[PageElement] = soup.find(id='tab-description').contents
        name = soup.find(class_='product_title entry-title').string

        return r.status_code, content, name
    else:
        return r.status_code, [], None


def compute_tags(content: List[PageElement]) -> Dict[str, Any]:
    fields: Dict[str, Any] = {}

    it: Iterator[PageElement] = enumerate(content)

    for i, tag in it:
        if tag.name == 'h3' and tag.text.strip().lower() == 'sfida':
            (i, tag) = next(it)
            match: Match = re.match(r'(\d+)/?(\d*) *\((\d+\.?\d*) *PE\)', tag.text)
            fields['challenge'] = float(match[1]) if not match[2] else float(match[1]) / float(match[2])
            fields['experience'] = int(match[3].replace('.', ''))

        elif tag.name == 'h3' and tag.text.strip().lower() == 'classe armatura':
            (i, tag) = next(it)
            match: Match = re.match(r'(\d+)( *\((.+)\))?', tag.text)
            fields['armorClass'] = int(match[1])
            if match[3]:
                fields['armorClassType'] = f'"{match[3]}"'

        elif tag.name == 'h3' and tag.text.strip().lower() == 'punti ferita':
            (i, tag) = next(it)
            match: Match = re.match(r'(\d+) *\((.+)\)', tag.text)
            fields['hitPoints'] = int(match[1])
            fields['hitPointsDices'] = f'"{match[2]}"'

        elif tag.name == 'h2' and is_list_field(tag.text):
            read_list(content[i + 1:], tag.text, fields)

        elif tag.name == 'figure' or tag.table:
            read_table(tag.table, fields)

        else:
            # caso default
            name = get_name_mapping(tag.text)
            if name:
                (i, tag) = next(it)
                fields[name] = f'"{tag.text}"'

    fields['passiveActions'] = read_passive_abilities(content)
    return fields


def get_name_mapping(field_name: str) -> Optional[str]:
    """
    Restituisce il nome in Kotlin del campo a partire dal campo originario
    """
    return __NAME_MAPPING.get(field_name.strip().lower())


def is_list_field(field_name: str) -> bool:
    """
    Restituisce True se il campo contiene una lista di valori che vanno concatenati con i separatori # e @
    """
    return field_name.strip().lower() in __LIST_FIELDS


def read_table(table: PageElement, fields: Dict[str, Any]) -> None:
    """
    Legge la tabella delle statistiche
    """
    rows = table.find_all_next('tr')

    for row in rows:
        cells = row.find_all_next('td')
        if cells and len(cells) >= 3:
            name = get_name_mapping(cells[0].text)
            modifier_name = f'{name}Modifier'
            value = int(cells[1].text)
            modifier_value = int(cells[2].text) if cells[2].text != '-+0' else 0

            fields[name] = int(value)
            fields[modifier_name] = int(modifier_value)


def read_list(content: List[PageElement], field_name: str, fields: Dict[str, Any]) -> None:
    """
    Legge un campo di tipo lista e lo salva come stringa concatenata usando # e @
    """
    name = get_name_mapping(field_name)

    if content[0].name == 'p':
        description_name = f'{name}Description'
        description = re.sub(r"< *br */? *>", " ", content[0].text)

        fields[description_name] = f'"{description}"'

        content.pop(0)

    content = list(takewhile(lambda pe: pe.name != 'h2', content))

    headers = (x.text for x in content if x.name != 'p')
    paragraphs = (x.text for x in content if x.name == 'p')

    actions = (f'{act}#{re.sub(r"< *br */? *>", " ", desc)}' for act, desc in zip(headers, paragraphs))

    fields[name] = f"\"{'@'.join(actions)}\""


def read_passive_abilities(content: List[PageElement]) -> str:
    """
    Legge tutti i campi non mappati considerandoli abilità passive
    """
    tags = ((i, t) for (i, t) in enumerate(content) if t.name == 'h3' and not get_name_mapping(t.text))  # fixme

    headers = (h.text for _, h in tags)
    paragraphs = (content[i + 1].text for i, _ in tags)

    abilities = (f'{act}#{re.sub(r"< *br */? *>", " ", desc)}' for act, desc in zip(headers, paragraphs))

    return f"\"{'@'.join(abilities)}\""


def to_kotlin_code(fields: Dict[str, Any]) -> str:
    prefix = 'result.add(\n\tMonster(\n\t\t'

    body = ',\n\t\t'.join((f'{k} = {v}' for k, v in fields.items()))

    postfix = '\n\t)\n)\n\n\n'

    return prefix + body + postfix


def main():
    url_mostri = []

    with open("./URL_Mostri.txt", "r") as file_mostri:
        url_mostri = [x.strip() for x in file_mostri.readlines() if len(x.strip()) > 0]

    shuffle(url_mostri)

    failures = []

    with open('result_mostri.txt', 'w', encoding='utf-8') as out:
        for index, url in enumerate(url_mostri):
            try:
                print(f'{index + 1} di {len(url_mostri)} - {url}')
                r = requests.get(url)
                (resp, content, name) = get_content(r)
                if resp != 200:
                    print(resp)
                    quit(1)
                else:
                    fields = compute_tags(content)
                    fields['name'] = f'"{name}"'
                    out.write(to_kotlin_code(fields))
            except Exception as e:
                print(f'ERRORE: {str(e)}')
                failures.append(url)
            time.sleep(randint(1, 3))

    print(f'{len(url_mostri)} URL elaborate ({len(url_mostri) - len(failures)} successi, {len(failures)} fallimenti)')

    if failures:
        with open('errori_mostri.txt', 'w', encoding='utf-8') as err:
            err.write('\n'.join(failures))


if __name__ == '__main__':
    main()
