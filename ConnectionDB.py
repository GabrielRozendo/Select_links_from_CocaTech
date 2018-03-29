import pymongo
import datetime
import configparser
from LogObj import Escrever, EscreverTela, EscreverLog
from enum import Enum


appConfig = configparser.ConfigParser()
appConfig.read("App.ini")
connection = appConfig.get("Connection", "uri")

uri = 'mongodb://'+connection+'?ssl=true&ssl_cert_reqs=CERT_NONE&replicaSet=globaldb'
client = pymongo.MongoClient(uri)
db = client.SelectLinks


def GetDate():
    return str(datetime.datetime.now())

#region Posts

class PostFeed(object):
    def __init__(self, title, tags, link, data, origem):
        self.title = title
        self.tags = tags
        self.link = link
        self.data = data
        self.origem = origem

def InsertPost(Post):
    try:
        db.Posts.insert_one(
            {
            "title": Post.title,
            "link": Post.link,
            "data": Post.data,
            "tags": Post.tags,
            "origem": Post.origem,
            "criadoEm": GetDate()
            })
        Escrever ('Post {} do {} salvo com sucesso!'.format(Post.title, Post.origem))

    except Exception as e:
        Escrever ('Exceção no insert de post: {}'.format(str(e)))


def ReadPost():
    try:
        posts = db.Posts.find()
        EscreverTela ('Lendo todos posts salvos:')
        for p in posts:
            EscreverTela ('{} de {}. Em {}'.format(p.title, p.origem, p.data))

    except Exception as e:
        Escrever ('Exceção no read: {}'.format(str(e)))


def PostExists(link):
    try:
        posts = db.Posts.find({'link':link}).limit(1)
        
        if posts.count() == 0: 
            #EscreverTela ('Post NÃO existe: \t--\t{}'.format(posts[0]['title']))
            return False
        else:
            #EscreverTela ('Post já existe: \t--\t\t{}'.format(posts[0]['title']))
            return True

    except Exception as e:
        Escrever ('Exceção no exists: {}'.format(str(e)))


def ReadAllPosts():
    try:
        return list(db.Posts.find())
    except Exception as e:
        Escrever ('Exceção no readAll: {}'.format(str(e)))


def ReadPostsDaOrigem(origem):
    try:
        posts = db.Posts.find({'origem':origem})
        EscreverTela ('Lendo todos posts com origem:'+origem)
        for p in posts:
            EscreverTela ('{} de {}. Em {}'.format(p.title, p.origem, p.data))

    except Exception as e:
        Escrever ('Exceção no readOrigem: {}'.format(str(e)))


def UpdatePost(link, Post):
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
        EscreverTela ("Atualizado!")

    except Exception as e:
        Escrever ('Exceção no update: {}'.format(str(e)))


def DeletePost(link):
    try:
        db.Posts.delete_many({"link":link})
        EscreverTela ('Apagado!')
    except Exception as e:
        Escrever ('Exceção no delete: {}'.format(str(e)))


def DropPosts():
    try:
        db.Posts.drop()
    except Exception as e:
        Escrever ('Exceção no drop: {}'.format(str(e)))
#endregion

#region Links

class TipoLink(Enum):
    AppStore = 'Apple Store (iOS)',
    Mac = 'Mac Store',
    PlayStore = 'Google Play Store (Android)',
    News = 'Notícias'

class LinkObj(object):
    def __init__(self, fonte, titulo, url, tipoLink):
        self.fonte = fonte
        self.titulo = titulo
        self.url = url
        self.tipo = tipoLink

def InsertLink(linkObj):
        try:
            db.Links.insert_one(
            {
            "fonte": linkObj.fonte,
            "titulo": linkObj.titulo,
            "url": linkObj.url,
            "tipo": linkObj.tipo,
            "criadoEm": GetDate()
            })
            Escrever ('Link ({}) {}: {} de {} salvo com sucesso!'.format(linkObj.tipo, linkObj.titulo, linkObj.url, linkObj.fonte))

        except Exception as e:
            Escrever ('Exceção no insert de link: {}'.format(str(e)))
#endregion

def InsertLog(logObj):
    try:
        db.Logs.insert_one(logObj)
        EscreverTela ('Log salvo com sucesso!')

    except Exception as e:
        Escrever ('Exceção no InsertLog: {}'.format(str(e)))
