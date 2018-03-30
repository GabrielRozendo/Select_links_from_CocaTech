import requests
from bs4 import BeautifulSoup
import ConnectionDB
from Crawlers_parse import (GetAreaTransferencia, GetCocaTech, GetDefault, GetLoopMatinal)
from LogObj import Erro, Escrever


def Crawler(sourceTitle, url):
    try:
        Escrever('Crawler da página: {}'.format(url))
        response = requests.get(url)
        Escrever('Código do status de resultado: {}. Ok: {}'.format(response.status_code, response.ok))
        link = response.url.split('?', 1)[0]
        Escrever('Link {}\t\tOriginal: {}'.format(link, response.url))

        if response.ok:
            soup = BeautifulSoup(response.content, 'html.parser')
            Escrever('Página recuperada: {}'.format(soup.title.text))
            return Switch(sourceTitle, soup, link)
        else:
            Escrever('Página não recuperada...')
            return False
    except Exception as e:
        Erro(str(e))
        return False


def Switch(sourceTitle, soup, link):
    try:
        if 'CocaTech' in sourceTitle:
            return GetCocaTech(link, soup)
        elif 'Área de Transferência' in sourceTitle:
            return GetAreaTransferencia(link, soup)
        elif 'Loop Matinal' in sourceTitle:
            return GetLoopMatinal(link, soup)
        else:
            Escrever('Source não encontrado: {}'.format(sourceTitle))
            return GetDefault(link, soup)
    except Exception as e:
        Erro(str(e))
        return False
