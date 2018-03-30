import configparser
import pymongo
from Classes import GetDate
from LogObj import Escrever, EscreverLog, EscreverTela

appConfig = configparser.ConfigParser()
appConfig.read("App.ini")
connection = appConfig.get("Connection", "uri")

uri = 'mongodb://'+connection+'?ssl=true&ssl_cert_reqs=CERT_NONE&replicaSet=globaldb'
client = pymongo.MongoClient(uri)
db = client.SelectLinks


# region Posts
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
        Escrever('Post {} do {} salvo com sucesso!'.format(
            Post.title, Post.origem))

    except Exception as e:
        Escrever('Exceção no insert de post: {}'.format(str(e)))


def ReadPost():
    try:
        posts = db.Posts.find()
        EscreverTela('Lendo todos posts salvos:')
        for p in posts:
            EscreverTela('{} de {}. Em {}'.format(p.title, p.origem, p.data))

    except Exception as e:
        Escrever('Exceção no read: {}'.format(str(e)))


def PostExists(link):
    try:
        posts = db.Posts.find({'link': link}).limit(1)

        if posts.count() == 0:
            #EscreverTela ('Post NÃO existe: \t--\t{}'.format(posts[0]['title']))
            return False
        else:
            #EscreverTela ('Post já existe: \t--\t\t{}'.format(posts[0]['title']))
            return True

    except Exception as e:
        Escrever('Exceção no exists: {}'.format(str(e)))


def ReadAllPosts():
    try:
        return list(db.Posts.find())
    except Exception as e:
        Escrever('Exceção no readAll: {}'.format(str(e)))


def QtPosts():
    return len(ReadAllPosts())


def ReadPostsDaOrigem(origem):
    try:
        posts = db.Posts.find({'origem': origem})
        EscreverTela('Lendo todos posts com origem:'+origem)
        for p in posts:
            EscreverTela('{} de {}. Em {}'.format(p.title, p.origem, p.data))

    except Exception as e:
        Escrever('Exceção no readOrigem: {}'.format(str(e)))


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
        EscreverTela("Atualizado!")

    except Exception as e:
        Escrever('Exceção no update: {}'.format(str(e)))


def DeletePost(link):
    try:
        db.Posts.delete_many({"link": link})
        EscreverTela('Apagado!')
    except Exception as e:
        Escrever('Exceção no delete: {}'.format(str(e)))


def DropPosts():
    try:
        Escrever('Drop de todos posts. Havia: {}'.format(QtPosts()))
        db.Posts.drop()
        Escrever('Sucesso no drop! Conferindo quantidade: {}'.format(QtPosts()))
    except Exception as e:
        Escrever('Exceção no drop: {}'.format(str(e)))
# endregion

# region Links


def InsertLink(linkObj):
    try:
        db.Links.insert_one(
            {
                "fonte": linkObj.fonte,
                "titulo": linkObj.titulo,
                "postUrl": linkObj.postUrl,
                "link": linkObj.link,
                "tipo": linkObj.tipo,
                "criadoEm": GetDate()
            })
        Escrever('Link ({}) {}: {} de {} salvo com sucesso!'.format(
            linkObj.tipo, linkObj.titulo, linkObj.link, linkObj.fonte))

    except Exception as e:
        Escrever('Exceção no insert de link: {}'.format(str(e)))


def ReadAllLinks():
    try:
        return list(db.Links.find())
    except Exception as e:
        Escrever('Exceção no readAll: {}'.format(str(e)))


def QtLinks():
    return len(ReadAllLinks())


def DropLinks():
    try:
        Escrever('Drop de todos links. Havia: {}'.format(QtLinks()))
        db.Links.drop()
        Escrever('Sucesso no drop! Conferindo quantidade: {}'.format(QtLinks()))
    except Exception as e:
        Escrever('Exceção no drop: {}'.format(str(e)))
# endregion


def InsertLog(logObj):
    try:
        db.Logs.insert_one(logObj)
        EscreverTela('Log salvo com sucesso!')

    except Exception as e:
        Escrever('Exceção no InsertLog: {}'.format(str(e)))
