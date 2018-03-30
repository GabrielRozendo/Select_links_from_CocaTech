import ConnectionDB
from LogObj import Erro, Escrever
from Classes import LinkObj, TipoLink 


def SalvarLinks(links):
    try:
        for link in links:
            ConnectionDB.InsertLink(link)
        return True
    except Exception as e:
        Erro(str(e))
        return False


def GetCocaTech(link, soup):
    body = soup.find('div', class_='instapaper_body')

    links = []
    for iframe in body.find_all('iframe'):
        Escrever('IFrame encontrado {}'.format(iframe))
        links.append(LinkObj('Coca Tech', soup.title.text, link, iframe, TipoLink.Video))

    for a in body.find_all('a'):
        links.append(LinkObj('Coca Tech', soup.title.text, link, a, TipoLink.Video))
        Escrever('{} --> {}'.format(a.text, a['href']))

    for app in body.find_all('div', class_='wpappbox'):
        divIcon = app.find('div', class_='appicon')
        icon = divIcon.find('img')
        icon = 'https:' + icon['src']

        divTitle = app.find('a', class_='apptitle', href=True)
        #href = divTitle['href']
        title = divTitle['title']

        divDeveloper = app.find('div', class_='developer')
        developerName = divDeveloper.a.string

        divPrice = app.find('div', class_='price')
        price = divPrice.text

        if 'macappstore' in app.attrs['class']:
            store = TipoLink.Mac
        elif 'appstore' in app.attrs['class']:
            store = TipoLink.AppStore
        else:
            store = TipoLink.Desconhecido

        Escrever('App {} || by {}, {}'.format(title, developerName, price))
        Escrever('Link ({}): {}'.format(store, link))
        Escrever('----------------------------')

        links.append(LinkObj('Coca Tech', soup.title.text, link, app, store))

    return SalvarLinks(links)


def GetLoopMatinal(link, soup):
    links = []
    for a in soup.find_all('a'):
        links.append(LinkObj('Loop Matinal', soup.title.text, link, a, TipoLink.Desconhecido))
        Escrever('{} --> {}'.format(a.text, GetHref(a)))

    return SalvarLinks(links)


def GetAreaTransferencia(link, soup):
    links = []
    for a in soup.find_all('a'):
        links.append(LinkObj('Área de Transferência', soup.title.text, link, a, TipoLink.Desconhecido))
        Escrever('{} --> {}'.format(a.text, GetHref(a)))

    return SalvarLinks(links)


def GetDefault(link, soup):
    links = []
    for a in soup.find_all('a'):
        links.append(LinkObj('Desconhecido', soup.title.text, link, a, TipoLink.Desconhecido))
        Escrever('{} --> {}'.format(a.text, GetHref(a)))

    return SalvarLinks(links)


def GetHref(a):
    if 'href' in a:
        return a['href']
    else:
        return ''