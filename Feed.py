import feedparser
import time
import json

url = 'http://feeds.cocatech.com.br/cocatechpodcast'
feed = feedparser.parse(url)

class PostFeed(object):
    def __init__(self, title, tags, link, data):
        self.title = title
        self.tags = tags
        self.link = link
        self.data = data


posts = []

for post in feed.entries:
    post_tags = []
    for tag in post.tags:
        post_tags.append(tag['term'])    
    tags = ", ".join(post_tags)
    postItem = PostFeed(post.title, tags, post.link, post.published)
    posts.append(postItem)
    
tagAnterior = ''
for post in posts:
    if tagAnterior != post.tags:
        print('Tags diferentes!')
        tagAnterior = post.tags
    
    print('Titulo: {}'.format(post.title))
    print('Postado em: {} -- com as tags: {}'.format(post.data, post.tags))
    print('Link: {}'.format(post.link))
    print("-----------------------------------------\n")
