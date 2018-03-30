import feedparser
import ConnectionDB
from Classes import PostFeed
from LogObj import Escrever, EscreverLog, EscreverTela, Inicio, FinalizarLog, Alterado, Sucesso, Erro
from Crawler import Crawler

try:

    # ConnectionDB.DropPosts()
    # ConnectionDB.DropLinks()
    EscreverTela('Qt de posts existentes: {}'.format(ConnectionDB.QtPosts()))
    EscreverTela('Qt de links existentes: {}'.format(ConnectionDB.QtLinks()))

    Inicio()
    novoPostSalvo = False

    with open('Sources.txt') as txt:
        fontes = txt.readlines()
        # remove whitespace characters like '\n' at the end of each line
        fontes = [x.strip() for x in fontes]

    for fonte in fontes:
        # split = fonte.split(' ')
        # fonteEnum = split[0]
        # fonteUrl = split[1]
        # Escrever('Acessando a fonte {}: {}'.format(fonteEnum, fonteUrl))
        Escrever('Acessando a fonte: {}'.format(fonte))


        try:
            novoPostNesseFeed = False
            rss = feedparser.parse(fonte)
            Escrever('Resultado do parse: {}'.format(rss.status))
            title = rss.feed.title
            Escrever('Feed {} atualizado em {} e possui {} itens...'.format(
                title, rss.updated, len(rss.entries)))

            for post in rss.entries:
                if not ConnectionDB.PostExists(post.link):
                    Escrever('Novo post encontrado...')
                    if(Crawler(title, post.link)):
                        novoPostNesseFeed = True
                        novoPostSalvo = True
                        post_tags = []
                        for tag in post.tags:
                            post_tags.append(tag['term'])
                        tags = "; ".join(post_tags)
                        postItem = PostFeed(post.title, tags, post.link, post.published, rss.title)
                        ConnectionDB.InsertPost(postItem)
                    else:
                        Escrever('Crawler deu erro :(')
            if not novoPostNesseFeed:
                Escrever('Nada novo encontrado nesse feed...')

        except Exception as e:
            Erro(str(e))

        finally:
            Escrever('------------')

    Alterado(novoPostSalvo)

    posts = ConnectionDB.ReadAllPosts()
    Escrever('Posts salvos nesse momento: {}'.format(len(posts)))
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
