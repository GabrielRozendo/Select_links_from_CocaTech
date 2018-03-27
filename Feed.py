import feedparser
import ConnectionDB
import LogObj

try:

    qt=len(ConnectionDB.readAll())
    print ('Qt de docs existentes: {}'.format(str(qt)))


    LogObj.Inicio()

    class Fonte(object):
        def __init__(self, link, nome):
            self.link = link
            self.nome = nome


    class PostFeed(object):
        def __init__(self, title, tags, link, data, origem):
            self.title = title
            self.tags = tags
            self.link = link
            self.data = data
            self.origem = origem


    fontes = []
    fontes.append(Fonte('http://feeds.cocatech.com.br/cocatechpodcast', 'Site CocaTech'))


    for fonte in fontes:
            
        feed = feedparser.parse(fonte.link)
        for post in feed.entries:
            if not ConnectionDB.exists(post.link):
                post_tags = []
                for tag in post.tags:
                    post_tags.append(tag['term'])    
                tags = "; ".join(post_tags)
                postItem = PostFeed(post.title, tags, post.link, post.published, fonte.nome)
                
                ConnectionDB.insert(postItem)


    posts = ConnectionDB.readAll()
    for post in posts:
        print('Titulo: {}'.format(post['title']))
        print('Postado em: {} -- com as tags: {}'.format(post['data'], post['tags']))    
        print('Origem: {}\t\tLink: {}'.format(post['origem'], post['link']))
        print("-----------------------------------------\n")


    #ConnectionDB.drop()

except Exception as e:
    print (str(e))

finally:
    LogObj.FinalizarLog()