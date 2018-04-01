import requests
from bs4 import BeautifulSoup
import ConnectionDB
from Classes import InListAnyInS, LinkObj, TipoLink
from LogObj import Erro, Escrever


def GetPage(link, nivel):
    Escrever('Get Page: {}'.format(link))
    response = requests.get(link)
    Escrever('Código do status de resultado: {}. Ok: {}'.format(response.status_code, response.ok), nivel)
    if response.ok:
        return response
    else:
        Escrever('Página não recuperada...', nivel)
        return None


def GetHref(a):
    if 'href' in a.attrs:
        return a['href']
    else:
        return a


def TratarTipoLink(a):
    if InListAnyInS(['App Store', 'AppStore'], a.text):
        return TipoLink.AppStore
    elif InListAnyInS(['KickStarter', 'Indiegogo', 'Rockethub', 'GoFundme', 'Crowdrise', 'Kickante', 'startmeup', 'impulso', 'idea.me', 'catarse', 'vaquinha'], a.text):
        return TipoLink.Crowdfunding
    elif InListAnyInS(['GooglePlay', 'Google Play', 'Play Store'], a.text):
        return TipoLink.PlayStore
    elif InListAnyInS(['Youtube', 'Vimeo'], a.text):
        return TipoLink.Video
    else: 
        return TipoLink.News


def GetCocaTech(link, soup, nivel):
    body = soup.find('div', class_='instapaper_body')

    links = []
    for iframe in body.find_all('iframe'):
        #Escrever('IFrame encontrado {}'.format(iframe), nivel)
        links.append(LinkObj('Coca Tech', soup.title.text, link, iframe, TipoLink.Video).toJSON())

    for a in body.find_all('a'):
        links.append(LinkObj('Coca Tech', soup.title.text, link, a, TipoLink.News).toJSON())
        #Escrever('{} --> {}'.format(a.text, a['href']), nivel)

    for app in body.find_all('div', class_='wpappbox'):
        # divIcon = app.find('div', class_='appicon')
        # icon = divIcon.find('img')
        # icon = 'https:' + icon['src']

        # divTitle = app.find('a', class_='apptitle', href=True)
        #href = divTitle['href']
        # title = divTitle['title']

        # divDeveloper = app.find('div', class_='developer')
        # developerName = divDeveloper.a.string

        # divPrice = app.find('div', class_='price')
        # price = divPrice.text

        if 'macappstore' in app.attrs['class']:
            store = TipoLink.Mac
        elif 'appstore' in app.attrs['class']:
            store = TipoLink.AppStore
        else:
            store = TipoLink.Desconhecido

        #Escrever('App {} || by {}, {}'.format(title, developerName, price), nivel)
        #Escrever('Link ({}): {}'.format(store, link), nivel)
        #Escrever('----------------------------', nivel)

        links.append(LinkObj('Coca Tech', soup.title.text, link, app, store).toJSON())

    return links


def LinksDefault(fonte, postUrl, soup, nivel):
    links = []
    for a in soup.find_all('a'):
        texto = a.parent.text
        #texto = a.text
        link = GetHref(a)
        tipoLink = TratarTipoLink(a)
        links.append(LinkObj(fonte, texto, postUrl, link, tipoLink).toJSON())
        # Escrever('{} --> {}'.format(a.text, GetHref(a)), nivel)

    return links


def Crawler(fonteTitulo, postItem, nivel):
    # Escrever('Crawler da fonte {}'.format(fonteTitulo), nivel)
    
    if 'CocaTech' in fonteTitulo:
        response = GetPage(postItem.link, nivel+1)
        if response is not None:
            Escrever('Link da página: {}'.format(response.url), nivel)
            linkAjustado = response.url.split('?', 1)[0]            
            Escrever('Link Ajustado: {}'.format(linkAjustado), nivel)

            soup = BeautifulSoup(response.content, 'html.parser')
            Escrever('Página recuperada: {}'.format(soup.title.text), nivel)
            return GetCocaTech(linkAjustado, soup, nivel+1)
        else:
            return None
    else:
        soup = BeautifulSoup(postItem['content'][0].value, 'html.parser')
        return LinksDefault(fonteTitulo, postItem.link, soup, nivel+1)
