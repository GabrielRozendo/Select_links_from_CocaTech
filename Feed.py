import feedparser
import ConnectionDB

ConnectionDB.drop()
qt=len(ConnectionDB.readAll())
print ('Qt de docs existentes: {}'.format(str(qt)))

url = 'http://feeds.cocatech.com.br/cocatechpodcast'
feed = feedparser.parse(url)

class PostFeed(object):
    def __init__(self, title, tags, link, data, origem):
        self.title = title
        self.tags = tags
        self.link = link
        self.data = data
        self.origem = origem


for post in feed.entries:
    if not ConnectionDB.exists(post.link):
        post_tags = []
        for tag in post.tags:
            post_tags.append(tag['term'])    
        tags = "; ".join(post_tags)
        postItem = PostFeed(post.title, tags, post.link, post.published, "Site CocaTech")
        
        ConnectionDB.insert(postItem)


posts = ConnectionDB.readAll()
for post in posts:
    print('Titulo: {}'.format(post['title']))
    print('Postado em: {} -- com as tags: {}'.format(post['data'], post['tags']))    
    print('Origem: {}\t\tLink: {}'.format(post['origem'], post['link']))
    print("-----------------------------------------\n")
