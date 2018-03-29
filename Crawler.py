import requests
from bs4 import BeautifulSoup
import Crawlers_parse 
import ConnectionDB

def Crawler(source, url):
    page = requests.get(url)
    print(page.status_code)
    soup = BeautifulSoup(page.content, 'html.parser')
    print(soup.title.string)
    links = soup.a

    Switch(source, soup)

def Switch(source, soup):
    return {
        'Coca Tech': CocaTech(soup),
        'Área de Transferência': AreaTransferencia(soup),
        'Loop Matinal': LoopMatinal(soup)
    }.get(source, Default(soup))

def Default(soup):
    return Crawlers_parse.GetDefault(soup)

def CocaTech(soup):
    return Crawlers_parse.GetCocaTech(soup)

def AreaTransferencia(soup):
    return Crawlers_parse.GetAreaTransferencia(soup)

def LoopMatinal(soup):
    return Crawlers_parse.GetLoopMatinal(soup)
