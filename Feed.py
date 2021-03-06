import feedparser
from bs4 import BeautifulSoup

import ConnectionDB
import TelegramBotMsg
from Classes import PostFeed
from Crawler import Crawler
from LogObj import (Alterado, Erro, Escrever, EscreverLog, EscreverTela, EscreverTelaMesmaLinha, FinalizarLog, Inicio, Sucesso)


def NovoPostEncontrado(titulo, postItem, lstPosts, lstLinks, nivel):
    try:
        Escrever('Novo post encontrado de {}. Titulo: {}. Link: {}'.format(titulo, postItem.title, postItem.link), nivel)

        links = Crawler(titulo, postItem, nivel+1)
        if links is not None:
            lstLinks.extend(links)

            if 'tags' in postItem:
                post_tags = []
                for tag in postItem.tags:
                    post_tags.append(tag['term'])
                tags = "; ".join(post_tags)
            else:
                tags = None

            if 'published' in postItem:
                pubDate = postItem.published
            elif 'pubDate' in postItem:
                pubDate = postItem.pubDate
            else:
                pubDate = None

            EnviarViaTelegramBot(titulo, postItem.link, postItem.title, links)
            postItem = PostFeed(postItem.title, tags, postItem.link, pubDate, titulo)            
            lstPosts.append(postItem.toJSON())
            return True
        else:
            Escrever('Crawler não retornou links', nivel)
            return False

    except Exception as e:
        Erro('Exceção no novo post encontrado. Erro: {}'.format(str(e)))
        return False


def EnviarViaTelegramBot(titulo, postItemLink, postItemTitle, links):
    qt = len(links)
    i = 0
    plural = 's' if qt > 1 else ''
    # TelegramBotMsg.send_message('*{3}* novo{0} link{0} encontrado{0} em *{1}* -- _{2}_.'.format(plural, titulo, postItemTitle, qt))
    for link in links:
        i+=1
        soup = BeautifulSoup(link['link'], 'html.parser')
        href = soup.a['href']
        text = soup.text
        
        indice = '_{} de {}_\n'.format(i, qt) if qt > 1 else ''

        msg =  'Novo{0} link{0} de *{1}*\n'.format(plural, titulo)
        msg += '{}\n'.format(postItemTitle)
        msg += indice
        msg += '\n`{}`\n'.format(link['tipo'])
        if not href in text:
            msg += '{} -> '.format(href)
        msg += '{}\n\n\n'.format(text)
        msg += '[link do post]({})'.format(postItemLink.split('?', 1)[0])

        TelegramBotMsg.send_message(msg)

try:
    # ConnectionDB.DropPosts()
    # ConnectionDB.DropLinks()
    EscreverTela('Qt de posts existentes: {}'.format(ConnectionDB.QtPosts()))
    EscreverTela('Qt de links existentes: {}'.format(ConnectionDB.QtLinks()))

    Inicio()
    novoPostSalvo = False
    lstLinks = []
    lstPosts = []

    with open('Fontes.txt') as txt:
        fontes = txt.readlines()
        # remove whitespace characters like '\n' at the end of each line
        fontes = [x.strip() for x in fontes]

    for fonte in fontes:
        nivel = 0
        Escrever('Acessando a fonte: {}'.format(fonte), nivel)

        try:
            nivel += 1
            novoPostNesseFeed = False
            rss = feedparser.parse(fonte)
            Escrever('Resultado do parse: {}'.format(rss.status), nivel)
            rssTitle = rss.feed.title
            if 'updated' in rss:
                updated = rss.updated
            elif 'updated' in rss.feed:
                updated = rss.feed.updated
            elif 'published' in rss.feed:
                updated = rss.feed.published

            qtEntries = len(rss.entries)
            Escrever('Feed {} atualizado em {} e possui {} itens...'.format(rssTitle, updated, qtEntries), nivel)

            i = 0
            for postItem in rss.entries:
                i += 1
                EscreverTelaMesmaLinha('{} de {}\t'.format(i, qtEntries))
                if ConnectionDB.PostExists(postItem.link):
                    EscreverTela(' '*99, False, False)
                else:
                    EscreverTela('', False, True)
                    if NovoPostEncontrado(rssTitle, postItem, lstPosts, lstLinks, nivel):
                        novoPostNesseFeed = True

            EscreverTela('')
            if novoPostNesseFeed:
                novoPostSalvo = True
            else:
                Escrever('Nada novo encontrado nesse feed...', nivel)

        except Exception as e:
            Erro('Exceção ao tratar a fonte. Erro: {}'.format(str(e)))

        finally:
            nivel = 0
            Escrever('-'*30, nivel)

    if lstLinks: # not lstLinks:
        ConnectionDB.InsertLinkMany(lstLinks)
    
    if lstPosts: # len(lstPosts) > 0:
        ConnectionDB.InsertPostMany(lstPosts)


    Alterado(novoPostSalvo)

    #posts = ConnectionDB.ReadAllPosts()
    #Escrever('Posts salvos nesse momento: {}'.format(len(posts)), nivel)
    # for post in posts:
    #    print('Titulo: {}'.format(post['title']))
    #    print('Postado em: {} -- com as tags: {}'.format(post['data'], post['tags']))
    #    print('Origem: {}\t\tLink: {}'.format(post['origem'], post['link']))
    #    print("-----------------------------------------\n")

    # ConnectionDB.drop()
    Sucesso()
except Exception as e:
    Erro(str(e))

finally:
    FinalizarLog()
