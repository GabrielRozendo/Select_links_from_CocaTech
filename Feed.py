import feedparser
import ConnectionDB
from LogObj import Escrever, EscreverLog, EscreverTela, Inicio, FinalizarLog, Alterado, Sucesso, Erro
from Crawler import Crawler 

try:

    qt = len(ConnectionDB.ReadAllPosts())
    EscreverTela ('Qt de docs existentes: {}'.format(str(qt)))

    Inicio()
    novoFeed = False

    with open('Sources.txt') as txt:
        fontes = txt.readlines()
        #remove whitespace characters like '\n' at the end of each line
        fontes = [x.strip() for x in fontes]
   
    for fonte in fontes:
        Escrever('Acessando a fonte: {}'.format(fonte))

        try:
            alterado = False
            rss = feedparser.parse(fonte)
            Escrever('Resultado do parse: {}'.format(rss.status))
            title = rss.feed.title
            Escrever('Feed {} atualizado em {} e possui {} itens...'.format(title, rss.updated, len(rss.entries)))

            for post in rss.entries:
                if not ConnectionDB.PostExists(post.link):
                    Escrever('Novo post encontrado...')
                    alterado = True
                    novoFeed = True

                    Crawler(title, post.link)
                    
                    post_tags = []
                    for tag in post.tags:
                        post_tags.append(tag['term'])    
                    tags = "; ".join(post_tags)
                    postItem = PostFeed(post.title, tags, post.link, post.published, rss.title)
                    ConnectionDB.InsertPost(postItem)
            if not alterado:
                Escrever('Nada novo encontrado nesse feed...')

        except Exception as e:
            Erro(str(e))

        finally:
            Escrever('------------')
    
    Alterado(novoFeed)

    posts = ConnectionDB.ReadAllPosts()
    Escrever('Posts salvos nesse momento: {}'.format(len(posts)))
    #for post in posts:
    #    print('Titulo: {}'.format(post['title']))
    #    print('Postado em: {} -- com as tags: {}'.format(post['data'], post['tags']))    
    #    print('Origem: {}\t\tLink: {}'.format(post['origem'], post['link']))
    #    print("-----------------------------------------\n")


    #ConnectionDB.drop()
    Sucesso()
except Exception as e:
    Erro(str(e))

finally:
    FinalizarLog()