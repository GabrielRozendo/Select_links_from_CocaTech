def GetCocaTech(soup):
    apps = soup.find_all('div', class_='wpappbox')
    for app in apps:
        print()
        divIcon = app.find('div', class_='appicon')
        icon = divIcon.find('img')
        icon = 'https:' + icon['src']

        divTitle = app.find('a', class_='apptitle', href=True)
        link = divTitle['href']
        title = divTitle['title']
        
        divDeveloper = app.find('div', class_='developer')
        developerName = divDeveloper.a.string

        divPrice = app.find('div', class_='price')
        price = divPrice.text

        if 'macappstore' in app.attrs['class']:
            store = 'Mac'
        elif 'appstore' in app.attrs['class']:
            store = 'iOS'
        else:
            store = 'desconhecido!'

        print('App {}: {} || by {}, {}'.format(i, title, developerName, price))
        print('Link ({}): {}'.format(store, link))
        print('----------------------------')
    itens = []
    return itens

def GetLoopMatinal(soup):
    itens = []
    return itens

def GetAreaTransferencia(soup):
    itens = []
    return itens

def GetDefault(soup):
    itens = []
    return itens