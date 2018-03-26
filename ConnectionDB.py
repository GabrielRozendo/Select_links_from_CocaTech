import pymongo
import datetime
import ConfigParser

appConfig = ConfigParser.ConfigParser()
appConfig.read("App.ini")
connection = appConfig.get("Connection", "uri")

uri = 'mongodb://'+connection+'?ssl=true&replicaSet=globaldb'
client = pymongo.MongoClient(uri)

db = client.SelectLinks


def insert(Post):
    try:
        db.Posts.insert_one(
            {
            "title": Post.title,
            "link": Post.link,
            "data": Post.data,
            "tags": Post.tags,
            "origem": Post.origem,
            "criadoEm": str(datetime.datetime.now())
            })
        print ('Post {} do {} salvo com sucesso!'.format(Post.title, Post.origem))

    except Exception as e:
        print (str(e))


def read():
    try:
        posts = db.Posts.find()
        print ('Lendo todos posts salvos:')
        for p in posts:
            print ('{} de {}. Em {}'.format(p.title, p.origem, p.data))

    except Exception as e:
        print (str(e))


def exists(link):
    try:
        posts = db.Posts.find({'link':link}).limit(1)
        
        if posts.count() == 0: 
            #print ('Não existe')
            return False
        else:
            print ('Post: {} \t--\t\tjá existe!'.format(posts[0]['title']))
            return True

    except Exception as e:
        print (str(e))


def readAll():
    try:
        return list(db.Posts.find())
    except Exception as e:
        print (str(e))


def readOrigem(origem):
    try:
        posts = db.Posts.find({'origem':origem})
        print ('Lendo todos posts com origem:'+origem)
        for p in posts:
            print ('{} de {}. Em {}'.format(p.title, p.origem, p.data))

    except Exception as e:
        print (str(e))


def update(link, Post):
    try:
        db.Posts.update_one(
            {"link": link},
            {
            "$set": {
                 "title": Post.title,
                "data": Post.data,
                "tags": Post.tags,
                "origem": Post.origem
            }
            }
        )
        print ("Atualizado!")
    
    except Exception as e:
        print (str(e))


def delete(link):
    try:
        db.Posts.delete_many({"link":link})
        print ('Apagado!')
    except Exception as e:
        print (str(e))


def drop():
    try:
        db.Posts.drop()
    except Exception as e:
        print (str(e))