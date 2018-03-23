import requests
from bs4 import BeautifulSoup

url = 'https://cocatech.com.br/player-de-audiobook-compativel-com-itunes-e-audible-22-03'
url = 'https://cocatech.com.br/promocao-do-dia-22-03-2018'
page = requests.get(url)

print(page.status_code)
soup = BeautifulSoup(page.content, 'html.parser')

#<div class="wpappbox wpappbox-04237a9964f2b34c9aabf3b05b66ca6a appstore colorful simple">

print(soup.title.string)
print()

i = 0
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
    
    i += 1