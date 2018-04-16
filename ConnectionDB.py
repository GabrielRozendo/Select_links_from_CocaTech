import json

import pymongo

from AppConfig import GetConnectionURI
from Classes import GetDate
from LogObj import Escrever, EscreverLog, EscreverTela

connection = GetConnectionURI()

uri = 'mongodb://'+connection+'?ssl=true&ssl_cert_reqs=CERT_NONE&replicaSet=globaldb'
client = pymongo.MongoClient(uri)
db = client.SelectLinks


def InsertLog(logObj):
    try:
        db.Logs.insert_one(logObj)
        EscreverTela('Log salvo com sucesso!')

    except Exception as e:
        Escrever('Exceção no InsertLog: {}'.format(str(e)))


#region Posts
def InsertPost_(Post):
    try:
        db.Posts.insert_one(
            {
                "titulo": Post.title,
                "link": Post.link,
                "data": Post.data,
                "tags": Post.tags,
                "origem": Post.origem,
                "criadoEm": GetDate()
            })
        Escrever('Post {} do {} salvo com sucesso!'.format(Post.title, Post.origem))

    except Exception as e:
        Escrever('Exceção no insert de post: {}'.format(str(e)))


def InsertPostMany(posts):
    try:
        qt = len(posts)
        Escrever('Posts recebidos para salvar: {}'.format(qt))
        result = db.Posts.insert_many(posts)
        qtResult = len(result.inserted_ids)
        Escrever('{} posts salvos com sucesso! Qt equivalente: {}'.format(qtResult, str(qt == qtResult)))
    except Exception as e:
        Escrever('Exceção no insert post many: {}'.format(str(e)))


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
        return bool(db.Posts.find_one({'link': link}))
    except Exception as e:
        Escrever('Exceção no exists: {}'.format(str(e)))


def ReadAllPosts():
    try:
        return list(db.Posts.find())
    except Exception as e:
        Escrever('Exceção no readAll: {}'.format(str(e)))


def QtPosts():
    return db.Posts.count()


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
                    "titulo": Post.title,
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
#endregion

#region Links

def InsertLink_(linkObj):
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
        Escrever('Link ({}) {}: {} de {} salvo com sucesso!'.format(linkObj.tipo, linkObj.titulo, linkObj.link, linkObj.fonte))

    except Exception as e:
        Escrever('Exceção no insert de link: {}'.format(str(e)))


def InsertLinkMany(links):
    try:
        qt = len(links)
        Escrever('Links recebidos para salvar: {}'.format(qt))
        result = db.Links.insert_many(links)
        qtResult = len(result.inserted_ids)
        Escrever('{} links salvos com sucesso! Qt equivalente: {}'.format(qtResult, str(qt == qtResult)))
    except Exception as e:
        Escrever('Exceção no insert link many: {}'.format(str(e)))


def ReadAllLinks():
    try:
        return list(db.Links.find())
    except Exception as e:
        Escrever('Exceção no readAll: {}'.format(str(e)))


def QtLinks():
    return db.Links.count()


def DropLinks():
    try:
        Escrever('Drop de todos links. Havia: {}'.format(QtLinks()))
        db.Links.drop()
        Escrever('Sucesso no drop! Conferindo quantidade: {}'.format(QtLinks()))
    except Exception as e:
        Escrever('Exceção no drop: {}'.format(str(e)))
#endregion

#region Telegram

def InsertTelegramConversation(nome, user, id):
    try:
        db.TelegramBot.insert_one({"nome": nome, "user": user, "id": id, "status": 1, "criadoEm": GetDate()})

        Escrever('ID Telegram salvo com sucesso: {} ({}) - {}!'.format(nome, user, id))
    except Exception as e:
        Escrever('Exceção no InsertTelegramConversation: {}'.format(str(e)))

 
def InativarTelegramConversation(id):
    try:
        db.TelegramBot.delete_one({"id": id})
        EscreverTela('Apagado!')
    except Exception as e:
        Escrever('Exceção no delete: {}'.format(str(e)))


def UsuarioAtivo(id):
    try:
        return bool(db.TelegramBot.find_one({'id': id, 'ativo': 1}))
    except Exception as e:
        Escrever('Exceção no exists: {}'.format(str(e)))
        return False


def ReadAllTelegramUsers():
    try:
        return list(db.TelegramBot.find())
    except Exception as e:
        Escrever('Exceção no ReadAllTelegramUsers: {}'.format(str(e)))


def QtTelegramUsers():
    return db.TelegramBot.count()

#endregion